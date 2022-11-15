from transformers import TensorFlowBenchmark, TensorFlowBenchmarkArguments

args = TensorFlowBenchmarkArguments(models=["deepset/roberta-base-squad2"])
benchmark = TensorFlowBenchmark(args)

results = benchmark.run()

print(results)