"""
COV-IA: Cognitive Optimization for AI Inference
Versión con modos correctamente diferenciados + integración Ollama
"""

import numpy as np
import random
import time
import subprocess
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

# ============================================================
# CONFIGURACIÓN DE MODOS (CORREGIDA)
# ============================================================
class COVMode(Enum):
    BALANCED = "balanced"
    PERFORMANCE = "performance"
    ULTRA = "ultra"
    PRECISION = "precision"


@dataclass
class ModeConfig:
    name: str
    target_accuracy: float
    max_latency_ms: float
    upgrade_threshold: float
    downgrade_threshold: float
    upgrade_cooldown: int
    allow_tiny: bool
    allow_small: bool
    allow_medium: bool
    allow_large: bool
    precision_fp32: bool
    precision_fp16: bool
    precision_int8: bool


MODE_CONFIGS = {
    COVMode.PRECISION: ModeConfig(
        name="Precision",
        target_accuracy=0.98,
        max_latency_ms=70,
        upgrade_threshold=-0.15,
        downgrade_threshold=0.08,
        upgrade_cooldown=25,
        allow_tiny=False,
        allow_small=False,
        allow_medium=True,
        allow_large=True,
        precision_fp32=True,
        precision_fp16=True,
        precision_int8=False
    ),
    COVMode.BALANCED: ModeConfig(
        name="Balanced",
        target_accuracy=0.96,
        max_latency_ms=40,
        upgrade_threshold=-0.1,
        downgrade_threshold=0.05,
        upgrade_cooldown=15,
        allow_tiny=False,
        allow_small=True,
        allow_medium=True,
        allow_large=True,
        precision_fp32=True,
        precision_fp16=True,
        precision_int8=False
    ),
    COVMode.PERFORMANCE: ModeConfig(
        name="Performance",
        target_accuracy=0.94,
        max_latency_ms=25,
        upgrade_threshold=-0.06,
        downgrade_threshold=0.03,
        upgrade_cooldown=10,
        allow_tiny=True,
        allow_small=True,
        allow_medium=True,
        allow_large=True,
        precision_fp32=True,
        precision_fp16=True,
        precision_int8=True
    ),
    COVMode.ULTRA: ModeConfig(
        name="Ultra",
        target_accuracy=0.90,
        max_latency_ms=15,
        upgrade_threshold=-0.03,
        downgrade_threshold=0.01,
        upgrade_cooldown=5,
        allow_tiny=True,
        allow_small=True,
        allow_medium=True,
        allow_large=True,
        precision_fp32=False,
        precision_fp16=True,
        precision_int8=True
    )
}


# ============================================================
# NÚCLEO RG - TCF v3.1
# ============================================================
class RG_Core:
    def __init__(self, a=0.5, b=0.8, c=0.3):
        self.a = a
        self.b = b
        self.c = c
        
    def separatrix(self, g6: float) -> float:
        return np.sqrt(self.b / 4) * min(1.5, g6)
    
    def dist_to_sep(self, g6: float, g9: float) -> float:
        return g9 - self.separatrix(g6)
    
    def iterate(self, g3: float, g6: float, g9: float, dt: float, perturbation: float = 0) -> Tuple:
        g9 = min(1.5, max(0, g9 + perturbation * 0.4))
        
        beta3 = self.c * g9
        beta6 = self.a * g3 * g3
        beta9 = -4.0 * g9 + self.b * g6 * g6
        
        return (
            min(1.5, max(0, g3 + beta3 * dt)),
            min(1.5, max(0, g6 + beta6 * dt)),
            min(1.5, max(0, g9 + beta9 * dt))
        )


# ============================================================
# SIMULADOR CON MODOS CORRECTOS
# ============================================================
class InferenceSimulator:
    def __init__(self, name: str, mode: COVMode = COVMode.BALANCED):
        self.name = name
        self.mode = mode
        self.config = MODE_CONFIGS[mode]
        
        self.model_sizes = {
            'tiny':   {'latency_ms': 8,   'accuracy': 0.92, 'cost': 1},
            'small':  {'latency_ms': 16,  'accuracy': 0.95, 'cost': 2},
            'medium': {'latency_ms': 32,  'accuracy': 0.97, 'cost': 4},
            'large':  {'latency_ms': 68,  'accuracy': 0.985, 'cost': 8}
        }
        
        # Iniciar según modo
        if mode == COVMode.PRECISION:
            self.current_model = 'large'
            self.precision = 'fp32'
        elif mode == COVMode.ULTRA:
            self.current_model = 'small'
            self.precision = 'int8'
        else:
            self.current_model = 'large'
            self.precision = 'fp32'
            
        self.history = []
        self.cooldown = 0
        
    def get_available_models(self) -> List[str]:
        """Retorna modelos disponibles según modo"""
        available = []
        cfg = self.config
        if cfg.allow_large: available.append('large')
        if cfg.allow_medium: available.append('medium')
        if cfg.allow_small: available.append('small')
        if cfg.allow_tiny: available.append('tiny')
        return available
    
    def get_available_precisions(self) -> List[str]:
        """Retorna precisiones disponibles según modo"""
        available = []
        if self.config.precision_fp32: available.append('fp32')
        if self.config.precision_fp16: available.append('fp16')
        if self.config.precision_int8: available.append('int8')
        return available
    
    def get_latency(self) -> float:
        base = self.model_sizes[self.current_model]['latency_ms']
        precision_factor = {'fp32': 1.0, 'fp16': 0.62, 'int8': 0.38}
        return base * precision_factor[self.precision]
    
    def get_accuracy(self) -> float:
        base = self.model_sizes[self.current_model]['accuracy']
        precision_penalty = {'fp32': 0, 'fp16': -0.007, 'int8': -0.016}
        return base + precision_penalty[self.precision]
    
    def get_cost(self) -> float:
        model_cost = self.model_sizes[self.current_model]['cost']
        precision_factor = {'fp32': 1.0, 'fp16': 0.52, 'int8': 0.3}
        return model_cost * precision_factor[self.precision]
    
    def infer(self, complexity: float) -> Dict:
        latency = self.get_latency() * (0.7 + 0.6 * complexity)
        return {
            'latency_ms': latency,
            'accuracy': self.get_accuracy(),
            'model': self.current_model,
            'precision': self.precision,
            'cost': self.get_cost()
        }
    
    def apply_cov_action(self, dist_to_sep: float):
        """COV con acción según modo"""
        
        self.cooldown = max(0, self.cooldown - 1)
        cfg = self.config
        available_models = self.get_available_models()
        available_precisions = self.get_available_precisions()
        
        model_rank = {'tiny': 0, 'small': 1, 'medium': 2, 'large': 3}
        current_rank = model_rank[self.current_model]
        
        # Colapso inminente -> bajar al mínimo
        if dist_to_sep > cfg.downgrade_threshold * 1.5:
            if current_rank > 0 and len(available_models) > 1:
                # Bajar un nivel
                new_rank = max(0, current_rank - 1)
                for m, r in model_rank.items():
                    if r == new_rank and m in available_models:
                        self.current_model = m
                        break
                # También bajar precisión si es posible
                if 'int8' in available_precisions:
                    self.precision = 'int8'
                return f"💀 EMERGENCY: {self.current_model}+{self.precision}"
        
        # Zona crítica -> reducir
        elif dist_to_sep > cfg.downgrade_threshold:
            if self.precision != 'int8' and 'int8' in available_precisions:
                self.precision = 'int8'
                return f"🔴 CRITICAL: {self.precision}"
            elif current_rank > 0:
                new_rank = max(0, current_rank - 1)
                for m, r in model_rank.items():
                    if r == new_rank and m in available_models:
                        self.current_model = m
                        break
                return f"🔴 CRITICAL: {self.current_model}"
        
        # Zona de advertencia
        elif dist_to_sep > 0:
            if self.precision != 'fp16' and 'fp16' in available_precisions:
                self.precision = 'fp16'
                return f"⚠️ ADJUST: {self.precision}"
        
        # Zona estable -> mantener
        elif dist_to_sep > cfg.upgrade_threshold:
            return "✅ STABLE"
        
        # Zona muy estable -> mejorar calidad
        else:
            if self.cooldown == 0:
                # Mejorar precisión primero
                if self.precision != 'fp32' and 'fp32' in available_precisions:
                    self.precision = 'fp32'
                    self.cooldown = cfg.upgrade_cooldown
                    return f"⬆️ UPGRADE: {self.precision}"
                # Mejorar modelo
                elif current_rank < 3 and 'large' in available_models:
                    self.current_model = 'large'
                    self.cooldown = cfg.upgrade_cooldown
                    return f"⬆️ UPGRADE: {self.current_model}"
        
        return "⏸️ IDLE"
    
    def step(self, load: float, dist_to_sep: float) -> Dict:
        if dist_to_sep != -999:
            action = self.apply_cov_action(dist_to_sep)
        else:
            action = "NO COV"
        
        n_queries = int(load * 30)
        if n_queries == 0:
            n_queries = 1
            
        total_latency = 0
        for _ in range(n_queries):
            complexity = random.uniform(0.3, 1.0)
            result = self.infer(complexity)
            total_latency += result['latency_ms']
        
        avg_latency = total_latency / n_queries
        
        record = {
            'model': self.current_model,
            'precision': self.precision,
            'latency': avg_latency,
            'accuracy': self.get_accuracy(),
            'cost': self.get_cost(),
            'action': action,
            'load': load
        }
        self.history.append(record)
        return record


# ============================================================
# GENERADOR DE CARGA
# ============================================================
def generate_realistic_load(t: float) -> float:
    base = 0.25
    peak1 = 0.7 * np.exp(-((t % 8) - 3)**2 / 3)
    peak2 = 0.9 * np.exp(-((t % 22) - 10)**2 / 10)
    
    crisis = 0
    if 10 < t < 18:
        crisis = 1.2
    if 30 < t < 40:
        crisis = 1.5
    if 50 < t < 58:
        crisis = 1.3
    
    return min(2.0, base + peak1 + peak2 + crisis)


# ============================================================
# SIMULACIÓN
# ============================================================
def run_mode_simulation(mode: COVMode, duration_seconds: int = 60) -> Dict:
    print(f"   Simulando {mode.value}...", end=" ", flush=True)
    
    rg = RG_Core()
    inference = InferenceSimulator("COV", mode=mode)
    
    g3, g6, g9 = 0.8, 0.25, 0.12
    dt = 0.1
    steps = int(duration_seconds / dt)
    
    latencies = []
    accuracies = []
    costs = []
    model_counts = {}
    
    for i in range(steps):
        t = i * dt
        load = generate_realistic_load(t)
        
        perturbation = load * 0.4
        g3, g6, g9 = rg.iterate(g3, g6, g9, dt, perturbation)
        
        dist = rg.dist_to_sep(g6, g9)
        result = inference.step(load, dist)
        
        latencies.append(result['latency'])
        accuracies.append(result['accuracy'])
        costs.append(result['cost'])
        model_counts[result['model']] = model_counts.get(result['model'], 0) + 1
    
    print("✓")
    
    return {
        'mode': mode.value,
        'avg_latency': np.mean(latencies),
        'p95_latency': np.percentile(latencies, 95),
        'avg_accuracy': np.mean(accuracies),
        'avg_cost': np.mean(costs),
        'models': model_counts,
        'total_steps': steps
    }


# ============================================================
# MAIN
# ============================================================
def main():
    print("\n" + "█"*70)
    print("🚀 COV-IA: Cognitive Optimization for AI Inference")
    print("   Basado en TCF v3.1 - Flujo RG con separatriz")
    print("   Modos configurables: Balanced | Performance | Ultra | Precision")
    print("█"*70)
    
    # Baseline SIN COV
    print("\n" + "="*70)
    print("📊 BASELINE: SIN COV")
    print("="*70)
    
    rg = RG_Core()
    g3, g6, g9 = 0.8, 0.25, 0.12
    dt = 0.1
    steps = int(60 / dt)
    latencies = []
    
    for i in range(steps):
        t = i * dt
        load = generate_realistic_load(t)
        perturbation = load * 0.4
        g3, g6, g9 = rg.iterate(g3, g6, g9, dt, perturbation)
        
        n_queries = int(load * 30)
        if n_queries == 0:
            n_queries = 1
        for _ in range(n_queries):
            # Simular modelo large + fp32
            latency = 68 * (0.7 + 0.6 * random.uniform(0.3, 1.0))
            latencies.append(latency)
    
    baseline_latency = np.mean(latencies)
    baseline_accuracy = 0.985
    baseline_cost = 8.0
    
    print(f"   Latencia media: {baseline_latency:.1f} ms")
    print(f"   Accuracy:       {baseline_accuracy:.4f}")
    print(f"   Costo:          {baseline_cost:.1f}")
    
    # Simular todos los modos
    print("\n" + "="*70)
    print("▶ EJECUTANDO SIMULACIONES POR MODO")
    print("="*70)
    
    results = []
    for mode in [COVMode.PRECISION, COVMode.BALANCED, COVMode.PERFORMANCE, COVMode.ULTRA]:
        result = run_mode_simulation(mode)
        results.append(result)
    
    # Mostrar tabla comparativa
    print("\n" + "="*70)
    print("🏆 COMPARATIVA DE MODOS COV")
    print("="*70)
    print(f"\n{'Modo':<12} {'Latencia':<12} {'vs Baseline':<12} {'Accuracy':<12} {'Costo':<10}")
    print("-"*70)
    
    for r in results:
        lat_improve = (baseline_latency - r['avg_latency']) / baseline_latency * 100
        acc_diff = r['avg_accuracy'] - baseline_accuracy
        cost_save = (baseline_cost - r['avg_cost']) / baseline_cost * 100
        
        acc_marker = "✅" if acc_diff >= -0.02 else "⚠️"
        
        print(f"{r['mode']:<12} {r['avg_latency']:.0f}ms      "
              f"-{lat_improve:.0f}%        "
              f"{r['avg_accuracy']:.4f} {acc_marker}   "
              f"-{cost_save:.0f}%")
        
        # Mostrar distribución de modelos
        total = r['total_steps']
        models_str = ", ".join([f"{m}:{c/total*100:.0f}%" for m, c in r['models'].items()])
        print(f"             └─ {models_str}")
    
    # Recomendación final
    print("\n" + "="*70)
    print("💡 RECOMENDACIÓN PARA EL HACKATHON")
    print("="*70)
    
    # Encontrar el mejor modo para cada caso
    best_balanced = min(results, key=lambda x: abs(x['avg_accuracy'] - 0.96))
    best_perf = min(results, key=lambda x: x['avg_latency'])
    best_precision = max(results, key=lambda x: x['avg_accuracy'])
    
    print(f"""
   📌 MODO PRECISION (Recomendado para alta precisión):
      - Latencia: {best_precision['avg_latency']:.0f}ms
      - Accuracy: {best_precision['avg_accuracy']:.4f}
      - Uso: Diagnóstico médico, finanzas, legal
    
   📌 MODO BALANCED (Recomendado por defecto):
      - Latencia: {best_balanced['avg_latency']:.0f}ms  
      - Accuracy: {best_balanced['avg_accuracy']:.4f}
      - Uso: Producción general, chatbots, asistentes
    
   📌 MODO PERFORMANCE (Recomendado para tiempo real):
      - Latencia: {best_perf['avg_latency']:.0f}ms
      - Accuracy: {best_perf['avg_accuracy']:.4f}
      - Uso: Juegos, streaming, tiempo real
    
   📌 MODO ULTRA (Recomendado para edge):
      - Latencia: {best_perf['avg_latency']:.0f}ms
      - Accuracy: {best_perf['avg_accuracy']:.4f}
      - Uso: Edge devices, batch, IoT
    """)
    
    print("\n   🔬 Basado en TCF v3.1 (Mendoza, 2025):")
    print("      - Flujo RG triádico con separatriz analítica")
    print("      - g₉ = √(b/4)·g₆ define frontera de colapso")
    print("      - COV anticipa y actúa antes del colapso")
    print("      - Modos configurables según caso de uso")
    
    return results


if __name__ == "__main__":
    main()