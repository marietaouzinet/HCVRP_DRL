# Deep Reinforcement Learning for Solving the Heterogeneous Capacitated Vehicle Routing Problem

## Introduction

As part of my engineering studies at Telecom Physique Strasbourg, I took part in an engineering project. The project was proposed by the city of Strasbourg, which wanted to make it easier for its employees to get around when distributing materials or equipment.

The aim of this project was to create an IT tool that could be run from a PC. The application allows employees to enter all the data relating to their deliveries via an input interface. This includes information such as delivery locations, type and number of materials to be delivered. The tool calculates the optimum route in terms of time and profitability, and informs the selection of the vehicle or vehicles to be used for the deliveries scheduled for the day. 

## Technical choices





Attention based model for learning to solve the Heterogeneous Capacitated Vehicle Routing Problem (HCVRP). Training with REINFORCE with greedy rollout baseline.



## Dependencies

* Python>=3.7
* NumPy
* SciPy
* [PyTorch](http://pytorch.org/)=1.3.0
* tqdm
* [tensorboard_logger](https://github.com/TeamHG-Memex/tensorboard_logger)
* Matplotlib (optional, only for plotting)