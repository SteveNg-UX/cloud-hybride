from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI, Form
import paramiko

app = FastAPI()

class Container(BaseModel):
    entrypoint: str
    start_stop: str
    container_name: str
    container_image: str | None = None
    container_port: str | None = None
    host_port: str | None = None

class Bdd(BaseModel):
    db_name: str
    db_user: str
    db_userpass: str

class VirtualMachine(BaseModel):
    vm_ip: str | None = None
    template: str | None = None
    disk_size: str | None = None
    number_worker: str | None = None
    deployement_name: str

def ssh_connection(ssh_command):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname="192.168.1.197", username="ansible", password="ansible")
        stdin, stdout, stderr = client.exec_command(ssh_command)
        output = stdout.read().decode()
        error = stderr.read().decode()
        client.close()
        return output, error
    except Exception as e:
        return None, str(e)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/api/docker/create_delete")
def create_delete_container(container: Container):
    if container.entrypoint == "web" and container.start_stop == "start":
        ssh_command = "ansible-playbook /ansible/docker_start_stop/ansible-playbook.yml -e 'entrypoint=web start_stop=start container_name="+container.container_name+" container_image="+container.container_image+"'"
    elif container.entrypoint == "other" and container.start_stop == "start":
        ssh_command = "ansible-playbook /ansible/docker_start_stop/ansible-playbook.yml -e 'entrypoint=other start_stop=start container_name="+container.container_name+" container_image="+container.container_image+" container_port="+container.container_port+" host_port="+container.host_port+"'"
    elif container.start_stop == "stop":
        ssh_command = "ansible-playbook /ansible/docker_start_stop/ansible-playbook.yml -e 'entrypoint=web start_stop=stop container_name="+container.container_name+"'"
    output, error =  ssh_connection(ssh_command)
    if error:
        return {"status": "error", "message": error}
    return {"status": "success", "output": output}

@app.post("/api/bdd/create")
def create_bdd(bdd: Bdd):
    ssh_command = "ansible-playbook /ansible/mysql_db_creation/ansible-playbook.yml -e 'db_name="+bdd.db_name+" db_user="+bdd.db_user+" db_userpass="+bdd.db_userpass+"'"
    output, error = ssh_connection(ssh_command)
    if error:
        return {"status": "error", "message": error}
    return {"status": "success", "output": output}

@app.post("/api/vm/create")
def create_vm(vm: VirtualMachine):
    async def send_data(
        vm_ip_create: str = Form(...),
        vm_name_create: str = Form(...),
        vm_template_create: str = Form(...),
        vm_storage_create: str = Form(...),
        vm_os_create: str = Form(...)
    ):
    payload = {
        "vm_ip_create": vm_ip_create,
        "vm_name_create": vm_name_create,
        "vm_template_create": vm_template_create,
        "vm_storage_create": vm_storage_create,
#        "vm_os_create": vm_os_create
    }
    ssh_command = "ansible-playbook /ansible/vm_create/ansible-playbook.yml -e 'vm_ip="+vm_ip_create+" template="+vm_template_create+" number_worker=0 disk_size="+vm_storage_create+" deployement_name="+vm_name_create+"'"
    output, error = ssh_connection(ssh_command)
    if error:
        return {"status": "error", "message": error}
    return {"status": "succes", "output": output}

@app.post("/api/vm/delete")
def delete_vm(deployement_name: str):
    ssh_command = "ansible-playbook /ansible/vm_destroy/ansible-playbook.yml -e 'deployement_name="+deployement_name+"'"
    output, error = ssh_connection(ssh_command)
    if error:
        return {"status": "error", "message": error}
    return {"status": "succes", "output": output}
