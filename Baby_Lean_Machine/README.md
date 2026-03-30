Last month, I learnt how to run an LLM locally on my computer with the goal of testing different LLMs' ability to generate logical, mathematical proofs and code. My idea was to train a personal model on any applied math code I wrote and test it's performance over time. I wanted to test how good basic LLMs had gotten at doing math and honestly just play around with this model.

# Baby LeanGCD

A local experiment inspired by the [LeanGCD research project](https://github.com/DeanLight/LeanGCD).

## What this is

I built a baby version of the LeanGCD feedback loop running entirely on my MacBook Pro using a local LLM. Instead of checking a proof only after it's fully generated, this script streams the model's output tactic by tactic and runs the Lean compiler after every line — catching mistakes early and feeding errors back into the model for the next attempt.

## How it works

1. A local LLM (deepseek-coder:6.7b via Ollama) generates a Lean 4 proof line by line
2. After each tactic, the Lean compiler checks if what's been written so far is already broken
3. If it is, generation aborts immediately and the error is fed back as context
4. The model retries up to 5 times with increasing error context
