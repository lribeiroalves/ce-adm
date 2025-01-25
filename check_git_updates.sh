#!/bin/bash

git fetch
commits=$(git log HEAD..origin/master --oneline)

if [ -z "$commits" ]; then
  echo "Seu branch está atualizado com 'origin/master'."
else
  echo "Há atualizações no branch remoto:"
  echo "$commits"
  # Descomente a linha abaixo para puxar as atualizações automaticamente
  # git pull
fi
