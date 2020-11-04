#!/usr/bin/env bash

echo "Running all metrics scripts for repository: $1"

docker volume create metrics

# Run Commits
cd Commits
./CommitsModule.sh $1 $2
cd ..

# Run Issues
cd Issues
./IssuesModule.sh $1 $2
cd ..

# Run GitModule
cd GitModule
./GitModule.sh $1
cd ..

# Run Issue_Spoilage
cd Issue_Spoilage
./IssueSpoilageModule.sh $1 $2
cd ..

# Run Defect Density (this command should also copy volume content to the current dir)
cd Defect_Density
./DefectDensityModule.sh $1 $2
cd ..

# Run Graph
cd Graph
./GraphModule.sh $1
cd ..



