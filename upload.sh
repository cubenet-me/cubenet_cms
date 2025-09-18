#!/bin/bash

echo "Выберите ветку для работы:"
echo "1) dev"
echo "2) main"
echo "3) release"
read -p "Ваш выбор (1/2/3): " branch_choice

# Определяем ветку
case $branch_choice in
  1)
    branch="dev"
    ;;
  2)
    branch="main"
    ;;
  3)
    branch="release"
    ;;
  *)
    echo "Неверный выбор. Выход."
    exit 1
    ;;
esac

# Переключаемся на выбранную ветку
git checkout $branch || { echo "Не удалось переключиться на ветку $branch"; exit 1; }

# Добавляем все изменения
git add -A
echo "Все изменения добавлены в staging area."

# Запрашиваем сообщение коммита
read -p "Введите сообщение коммита: " commit_msg
read -p "Подтвердить коммит? (Д/н): " confirm

if [[ $confirm == "Д" || $confirm == "д" || $confirm == "" ]]; then
  git commit -m "$commit_msg"
  git push origin $branch
  echo "Коммит и пуш выполнены в ветку $branch."
else
  echo "Коммит отменён."
fi
