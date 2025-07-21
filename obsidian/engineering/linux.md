- reinstall (force/overwrite) package with pacman
```bash
sudo pacman -S --overwrite \* <package-name>
sudo pacman -Qqn | sudo pacman -S --overwrite \* - # all packages
```