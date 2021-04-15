#!/usr/bin/env bash

read -p "Create new conda env (y/n)?" CONT

if [ "$CONT" == "n" ]; then
  echo "exit";

else
  echo "Creating new conda environment, choose name"
  read input_variable
  echo "Creating $input_variable";

  conda create --name $input_variable python=3.7

  eval "$(conda shell.bash hook)"
  conda activate $input_variable

  pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

  python main_shiori.py

  echo "to exit: source deactivate"

fi
