Some sample templates from https://cloud.google.com/deployment-manager/docs/step-by-step-guide/.

I mostly played around with the startup script, e.g.

```sh
#!/bin/bash
sudo apt-get install -y git
git clone https://github.com/carise/gcp-utils
ls
```
