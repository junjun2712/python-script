#!/data/.python-env/python3.8/bin/python3.8
import logging
import os, platform, sys, datetime
import tarfile
import subprocess
import parameter

def judge_os_type():
    os_type = platform.system()
    return os_type

def vm_compose_para_json(env):
    para_json = dict()
    if env == "develop":
        para_json['ssh_user'] = parameter.dev_ssh_user
        para_json['ssh_pass'] = parameter.dev_ssh_pass
        para_json['ssh_host'] = parameter.dev_ssh_host
        para_json['remote_copy_dir'] = parameter.dev_remote_copy_dir
        para_json['window_builder_pscp_bin_path'] = parameter.dev_window_builder_pscp_bin_path
        para_json['jenkins_job_name'] = parameter.dev_jenkins_job_name
        para_json['gitlab_repo_name'] = parameter.dev_gitlab_repo_name
        para_json['cocos_build_bin_path'] = parameter.dev_cocos_build_bin_path
        para_json['cocos_build_platform'] = parameter.dev_cocos_build_platform
        para_json['cocos_build_parameter'] = parameter.dev_cocos_build_parameter
        para_json['cocos_build_dir'] = parameter.dev_cocos_build_dir
        print(para_json)
    elif env == "test_new":
        para_json['ssh_user'] = parameter.test_ssh_user
        para_json['ssh_pass'] = parameter.test_ssh_pass
        para_json['ssh_host'] = parameter.test_ssh_host
        para_json['remote_copy_dir'] = parameter.test_remote_copy_dir
        para_json['window_builder_pscp_bin_path'] = parameter.test_window_builder_pscp_bin_path
        para_json['jenkins_job_name'] = parameter.test_jenkins_job_name
        para_json['gitlab_repo_name'] = parameter.test_gitlab_repo_name
        para_json['cocos_build_bin_path'] = parameter.test_cocos_build_bin_path
        para_json['cocos_build_platform'] = parameter.test_cocos_build_platform
        para_json['cocos_build_parameter'] = parameter.test_cocos_build_parameter
        para_json['cocos_build_dir'] = parameter.test_cocos_build_dir
        print(para_json)
    return  para_json

class cicd:
    def __init__(self, os_type, json_body):
        self.THIS_DIR = os.path.dirname(os.path.abspath(__file__))
        self.os_type = os_type
        self.para_json = json_body
        self.logging = logging
        self.separator = '\\' if self.os_type == 'Windows' else '/'
        self.build_res_dir = self.para_json['cocos_build_dir'] + self.separator + self.para_json['cocos_build_platform']
        self.commit_sha = self.get_commit_sha()
        self.version_file_path = self.build_res_dir + self.separator + "version.html"
        self.tar_file_name = "web-mobile-{}.tar.gz".format(self.commit_sha)
        self.tar_file_path = "{}{}web-mobile-{}.tar.gz".format(self.para_json['cocos_build_dir'], self.separator, self.commit_sha)
        self.tar_file_dir_path = os.path.join(self.para_json['cocos_build_dir'],self.para_json['cocos_build_platform'])

    def get_commit_sha(self):
        commit = ""
        gitlab_repo_dir = parameter.jenkins_workspace + self.separator +self.para_json['jenkins_job_name']
        if  os.path.isdir(gitlab_repo_dir):
            os.chdir(gitlab_repo_dir)
            res = os.popen("git rev-parse HEAD")
            commit = res.read()
            print("git commit SHA code: " + commit)
        return commit.strip()
    
    def create_version_file(self):
        with open(self.version_file_path, 'w', encoding='utf-8') as vf:
            vf.write(self.commit_sha)
    
    def get_version_file_commit(self):
        try:
            with open(self.version_file_path, 'r', encoding='utf-8') as vf:
                version_commit = vf.read()
            return version_commit.strip()  
        except Exception as e:
            print(e)
            
    def code_build(self):
        cocos_build_path = parameter.jenkins_workspace + self.separator + self.para_json['jenkins_job_name'] + \
                            self.separator + self.para_json['gitlab_repo_name']
        build_cmd = self.para_json['cocos_build_bin_path'] + " --path " + cocos_build_path + " --build platform=" + \
              self.para_json['cocos_build_platform'] + ";" + self.para_json['cocos_build_parameter']
        print('\n开始构建...\n', build_cmd)
        p = subprocess.run(build_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print('retun_code:', p.returncode)
        if p.returncode != 0:
            sys.exit('stdout: \n{}\n 构建失败!! 请检查!!'.format(p.stdout.decode('utf8')))
        else:
            print(p.stdout)
            print('\n构建成功\n')
                       

    def compression_build_file(self):
        print('tar_file_name:', self.tar_file_name)
        print('tar_file_path:', self.tar_file_path)
        print('tar_file_dir_path:', self.tar_file_dir_path)
        try:
            os.chdir(self.para_json['cocos_build_dir'])
            print(os.getcwd())
            tar = tarfile.open(self.tar_file_name,"w:gz")
            # 创建压缩包
            print('压缩打包....')
            # 这里遍历时如果写绝对路径,那打出来的包将包含绝对路径的目录层级,所以这里写相对路径
            for root,dir,files in os.walk(self.para_json['cocos_build_platform']):
                for file in files:
                    fullpath = os.path.join(root,file)
                    tar.add(fullpath)
            tar.close()
        except Exception as e:
            print(e)
    
    def upload_tar_file_to_download_server(self):
        host = self.para_json['ssh_host']
        username = self.para_json['ssh_user']
        password = self.para_json['ssh_pass']
        remote_copy_dir = self.para_json['remote_copy_dir']
        copy_cmd = self.para_json['window_builder_pscp_bin_path'] + " -l " + username + " -pw " + password \
          + " " + self.tar_file_path + " " + username  + "@" + host + ":" + remote_copy_dir
        print("上传压缩包到包管理站点...")
        print("upload cocos client program in " + host + " dir:" + remote_copy_dir)
        print('copy_cmd:', copy_cmd)
        os.system(copy_cmd)
        

    # def remote_copy(self, host, username, password ,remote_copy_dir):
        # cmd = self.para_json['window_builder_pscp_bin_path'] + " -l " + username + " -pw " + password \
          # + " -r " + self.para_json['cocos_build_dir'] + "\\" + self.para_json['cocos_build_platform'] + " " + username  +\
          # "@" + host + ":" + remote_copy_dir
        # print(cmd)
        # os.system(cmd)

# def ssh_cmd(host, username, password, cmd):
    # try:
        # ssh_fd = paramiko.SSHClient()
        # ssh_fd.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # print("ssh connecting " + host + " now ...")
        # ssh_fd.connect(host, username = username, password = password )
        # print("ssh connected ...")
        # stdin, stdout, stderr = ssh_fd.exec_command(cmd, get_pty = True)
        # stdin.write(password + '\n')
        # stdin.flush()
        # print(stdout.readlines())
        # print(cmd)
        # print(stderr.readlines())
        # ssh_fd.close()
        # print("ssh connect closed")
    # except Exception as e:
        # print( 'ssh %s@%s: %s' % (username, host, e) )
        # exit(1)

def get_parameter_from_jenkins():
    list_jenkins_para = list()
    if(len(sys.argv) != 2):
        print("Parameter Error!!!please give one para ENV")
        exit(888)
    else:
        env = sys.argv[1]
        list_jenkins_para.append(env)
    return list_jenkins_para

    
def main():
    # 接收jenkins参数
    list_jenkins_para = get_parameter_from_jenkins()
    env = list_jenkins_para.pop()
    os_type = judge_os_type()
    para_json = vm_compose_para_json(env)
    cicdops = cicd(os_type, para_json)
    
    print('current_commit_sha:',cicdops.commit_sha)
    print('last_version_commit:', cicdops.get_version_file_commit())
    if cicdops.commit_sha == cicdops.get_version_file_commit():
        print('当前版本已构建过，请不要重复构建')
        sys.exit(0)
    else:
        cicdops.code_build()
        cicdops.create_version_file()
        cicdops.compression_build_file()
        cicdops.upload_tar_file_to_download_server()
        try:
            os.remove(cicdops.tar_file_path)
        except FileNotFoundError as e:
            print(e)


if __name__ == '__main__':
    main()
