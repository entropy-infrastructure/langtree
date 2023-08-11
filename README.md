# Welcome to Langtree!

## What is Langtree

Langtree is a micro framework for building natively parallel LLM chains. Our goal is to keep the core of this repo under 100 LOC (not including test cases).

## Why use Langtree?

Langtree is dead simple. It's under 100 LOC for the core of the project. Seriously. *Theres only 3 constructs: Operators, Buffers, and Prompts.*

This means the following capabilities are **trivial**:

1. **Debuggability**: Langtree is *insanely* debuggable.
     It's so minimal that the underlying api's are almost identical to those exposed by our integrations.
     For example, the `messages` field on the `OpenAIChat` object is the exact field that is passed to the underlying api.
2. **Natively Parallel**: A common issue with LLM tools is parallelism. With Langtree, doing this is a piece of cake. This means Agents, retrieval, etc. are far quicker to iterate upon. *Make sure to read the docs before using the parallel tools*
3. **Langchain Interoperable**: Langtree can be used *with* Langchain. Although we are opinionated about Langtree, **Langchain offers a LOT of value**.
4. **Back Compatibility**: Expect Langtree to be extremely stable. Its so flexible that it *actually adjusts* when integrations change. It's only this capable because it is minimal. This is why we are commited to keeping the core library under 200 LOC. Forever.



## Features
### Chain recording
We offer a simple abstraction to record analytics on *any* chain **(Including Langchain code)**

We currently only have recording to JSON but expect to see more by 08/11/23

### Providers
Models: We currently support OpenAI.

## Roadmap
Function Calling: We plan to support function calls in the VERY near future.

Models: To support Azure, Huggingface (local and remote), Anthropic and Cohere

VectorDBs: Currently in development. Again we promise to maintain minimal levels of abstraction.

Recording: We are in the process of implementing S3, Planetscale, and more!
