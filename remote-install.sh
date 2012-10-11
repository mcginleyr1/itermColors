#!/bin/sh

ssh $1 'mkdir -p .zsh/bin'

rsync -avz husl.py $1:.zsh/bin/ &
rsync -avz rainbow-parade.py $1:.zsh/bin &
wait

ssh $1 'echo "python2.5 ~/.zsh/bin/rainbow-parade.py ~/.zsh/bin" >> ~/.bashrc' &
ssh $1 'echo "python2.5 ~/.zsh/bin/rainbow-parade.py ~/.zsh/bin" >> ~/.zshrc'
