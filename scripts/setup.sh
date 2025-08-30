#!/bin/bash
echo "setup.sh launched."
echo ""

# ユーザー名の入力
echo "Enter a username for Git."
echo "Press Enter to use the global setting."
echo "Type 'q' to cancel this script."
read -p "username >> " git_username

# 'q' なら終了
if [ "$git_username" = "q" ]; then
  echo ""
  echo "Script cancelled."
  exit 0
fi

if [ -z "$git_username" ]; then
  # グローバル設定から取得
  git_username=$(git config --global user.name)
  git_email=$(git config --global user.email)

  if [ -z "$git_username" ] || [ -z "$git_email" ]; then
    echo "Global Git username or email is not set."
    echo ""
    echo "Script cancelled."
    exit 1
  fi

  echo "Using global Git config:"
  echo "  user.name  = $git_username"
  echo "  user.email = $git_email"
else
  # メールアドレスの入力（ユーザー名が入力された場合のみ）
  echo ""
  echo "Enter an email for Git."
  echo "Type 'q' to cancel this script."
  read -p "email >> " git_email

  # 'q' なら終了
  if [ "$git_email" = "q" ]; then
    echo "Script cancelled."
    exit 0
  fi

  if [ -z "$git_email" ]; then
    echo "Error: email cannot be empty when a username is provided."
    echo ""
    echo "Script cancelled."
    exit 1
  fi
fi

# ローカル設定に反映
git config user.name "$git_username"
git config user.email "$git_email"

# 設定内容を確認
echo ""
echo "Local Git config updated:"
echo "  user.name  = $(git config --get user.name)"
echo "  user.email = $(git config --get user.email)"

# ファイル権限を gitの差分としない
git config --local core.fileMode false

echo ""
echo "Git setup succeed."
echo ""
