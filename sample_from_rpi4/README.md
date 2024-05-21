# RasPi4
Code for Raspberry Pi 4


# sshの設定メモ

```
$ cp id_rsa_git.pub /home/pi/.ssh/
$ cp id_rsa_git /home/pi/.ssh/
```

configファイルに設定を追加

```
Host github github.com
  HostName ssh.github.com
  Port 443
  IdentityFile ~/.ssh/id_rsa_git
  AddKeysToAgent yes
  User git
```

## 何度もパスフレーズを聞かれる件

ペンディング。MacとLinuxで異なるみたい。


## 接続のテスト

```
$ ssh -T git@github.com
```


# リモートにアップロード

```
$ git add .
$ git commit -m 'update README.md'
$ git push -u origin main
```

## 現在の設定

```
$ git remote -v
origin  github:mashi727/RasPi4.git (fetch)
origin  github:mashi727/RasPi4.git (push)
```