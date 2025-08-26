# One-Dimensional Packing of Dance Equipment

## Overview

This project addresses the logistical challenges faced by **UW Raas**, a competitive intercollegiate dance team, in transporting elaborate set designs to competitions across the US.

The set, based on the *Subway Surfers* theme, is constructed from PVC pipes of varying lengths. Airline and venue restrictions impose strict weight, dimension, and cost constraints on how these pipes are transported.

We developed an integer and linear programming model that:

- Generates a blueprint for assembling the set from the available inventory of pipes.
- Produces an optimized packing configuration for transporting the pipes in ski bags.
- Minimizes the number of bags required, balances weight distribution, and reduces travel costs.

## Problem Statement

**Given:**
- A set design requiring specific pipe lengths.
- A limited inventory of PVC pipes.
- A fixed number of ski bags with known capacity, dimensions, and airline weight limits.

**Find:**
- A pipe blueprint ensuring the design requirements are satisfied.
- A packing solution that fits pipes into the minimum number of ski bags without violating spatial or weight constraints.

## Methods

The model was implemented using **Gurobi** with binary decision variables:

- **Design blueprint variables** ensure that the required sides of the set are built from available pipe lengths.
- **Packing variables** allocate pipes to specific ski bags and rows, respecting spatial and weight constraints.
- **Linking constraints** ensure that the pipes selected in the blueprint are the same ones packed.

The **objective function** prioritizes:
1. Minimizing the number of bags used.  
2. Minimizing the number of rows used per bag (balanced packing).  
3. Minimizing the total number of pipes used (to simplify assembly).  

## Results

- Previous team solutions required **3-4 bags**.  
- Our optimized solution requires only **2 bags**, reducing travel costs and logistical complexity.  
- The packing configurations balanced weight and used up to **96% of available bag volume**.  

This model not only helps **UW Raas** but can be extended to construction, manufacturing, warehouse logistics, and event management, where cylindrical objects must be packed efficiently.

---

## Acknowledgements

This project was completed in collaboration with my project partners Mark and Benjamin. 
We would like to thank **Professor Sara Billey** for her guidance and **UW Raas** for providing real-world motivation and data.
