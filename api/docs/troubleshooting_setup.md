## Troubleshooting Setup

This is a reference to track setup and startup issues and nuances between different machines. 

### **Mac Machines**


### **Windows Machines**

- [StackOverflow question about activating venv on Windows](https://stackoverflow.com/questions/8921188/issue-with-virtualenv-cannot-activate)

- If you received the following error after running `bash startup.sh` or `docker compose up -d db`...

  <image src="api/docs/images/windows_docker_daemon_not_found.png"/>

- ...Or if you received the following prompt upon launching Docker Desktop...

  <image src="api/docs/images/windows_kernel_update.png"/>
  
  - Try running `wsl --update` in your shell, then close and re-launch Docker Desktop. Once Docker Desktop is running, try `docker compose up -d db` again. This worked for me.

</details>

<br/>
