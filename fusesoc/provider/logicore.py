from fusesoc.utils import pr_info, pr_err, Launcher
import os
import shutil

class Logicore(object):
    def __init__(self, core_name, config, core_root, cache_root):
        self.core_root    = core_root
        self.files_root   = cache_root
        self.script_file  = config.get('script_file')
        self.project_file = config.get('project_file')

    def fetch(self):
        status = self.status()
        if status != 'downloaded':
            self._checkout()
            return True
        return False

    def _checkout(self):
        pr_info("Using Xilinx Vivado to generate LogiCORE(tm) project " + self.project_file)
        if not os.path.isdir(self.files_root):
            os.mkdir(self.files_root)
        src_files = os.listdir(self.core_root)
        for f in src_files:
            f_src = os.path.join(self.core_root, f)
            if os.path.isdir(f_src):
                # skip directories
                continue
            f_dst = os.path.join(self.files_root, f)
            if(os.path.exists(f_src)):
                shutil.copyfile(f_src, f_dst)
            else:
                pr_err('Cannot find file %s' % f_src)
        args = ['-mode', 'batch',
                '-source', self.script_file]
        Launcher('vivado', args, cwd=self.files_root).run()

    def status(self):
        if not os.path.isdir(self.files_root):
            return 'empty'
        else:
            return 'downloaded'

PROVIDER_CLASS = Logicore
