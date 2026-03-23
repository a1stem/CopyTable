#!/bin/bash
set -e
echo "Deploying CopyTable to /opt/clipboard-app..."
sudo rsync -av \
  --exclude='.git' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  /home/cm/clipboard-app/ /opt/clipboard-app/
# Create terminal command symlink
sudo ln -sf /opt/clipboard-app/run.sh /usr/local/bin/copytable
sudo chown -R root:root /opt/clipboard-app
sudo chown -R cm:cm /opt/clipboard-app
echo "Done. Run with: copytable"
