# Proposal

## What will (likely) be the title of your project?

Modeling Disease Spread with the SIR Simulation in Python

## In just a sentence or two, summarize your project. (E.g., "A website that lets you buy and sell stocks.")

A Python simulation that models how an infectious disease spreads through a population over time using the
SIR (Susceptible–Infected–Recovered) model. The program will visualize how changes in transmission
and recovery rates affect the course of an outbreak.

## In a paragraph or more, detail your project. What will your software do? What features will it have? How will it be executed?

This project will simulate the dynamics of disease transmission using the SIR epidemiological model, which divides a population into three groups:
susceptible, infected, and recovered individuals. The user will be able to input parameters like population size, infection rate, and
recovery rate, and the program will simulate how those values evolve day by day.

I plan to use Python with libraries such as matplotlib to plot the number of susceptible, infected, and recovered individuals over time.
The program will show how adjusting infection rate and recovery rate changes the shape of the epidemic curve.
If I want to expand it later, I could add features like random variation, vaccination parameters, or geographic areas to simulate multiple
interacting populations.
The simulation will run in the terminal or a simple window, and all results (tables and plots) will be displayed at the end of each run.

## If planning to combine 1051's final project with another course's final project, with which other course? And which aspect(s) of your proposed project would relate to 1051, and which aspect(s) would relate to the other course?

N/A

## If planning to collaborate with 1 or 2 classmates for the final project, list their names, email addresses, and the names of their assigned TAs below.

N/A

## In the world of software, most everything takes longer to implement than you expect. And so it's not uncommon to accomplish less in a fixed amount of time than you hope.

### In a sentence (or list of features), define a GOOD outcome for your final project. I.e., what WILL you accomplish no matter what?

- Implement the basic SIR equations.

- Allow the user to input infection and recovery rates.

- Print day-by-day counts of S, I, R values.

### In a sentence (or list of features), define a BETTER outcome for your final project. I.e., what do you THINK you can accomplish before the final project's deadline?

- Add a matplotlib line plot showing S, I, R over time.

- Include adjustable parameters (e.g., total population, number of days).

- Automatically stop when the infection dies out.

### In a sentence (or list of features), define a BEST outcome for your final project. I.e., what do you HOPE to accomplish before the final project's deadline?

- Add interactive or animated visualization of disease spread.

- Include optional vaccination or reinfection.

- Save results (graphs or summary statistics) to a file.

- Possibly extend to a spatial model (disease spreading across a grid)

## In a paragraph or more, outline your next steps. What new skills will you need to acquire? What topics will you need to research? If working with one of two classmates, who will do what?

My next steps are to review the math behind the SIR model (the differential equations governing disease transmission) and decide whether to implement it
through simple loops or numerical approximation. I will learn how to use matplotlib for time-series plots and practice taking user input to adjust
parameters interactively. I will also research how to animate plots in real time and how to export data or figures.
