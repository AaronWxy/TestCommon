import os 

class SFTP(object):

    def __init__(self, Krakken):

        self.krakken = Krakken 
        self.sftp = None

    def open_sftp(self):

        self.krakken.ssh.fix_channel()
        self.sftp = self.krakken.ssh.connection.open_sftp()

    def close_sftp(self):

        if self.sftp:
            self.krakken.logger.info("Closing current sftp connection!")
            self.sftp.close() 

    def send_to_remote_path(self, local_path, remote_path):
        # check if remote path is a file or folder
        rc = self.krakken.ssh.blocking_call("test -d " + remote_path)
        if not rc:
            base_name = os.path.basename(local_path)
            remote_path += "/" + base_name
        self.krakken.logger.info("Sending local file {} to remote {}".format(local_path, remote_path))
        try:
            self.sftp.put(local_path, remote_path)
        except:
            self.krakken.logger.warn("Failed to send local file {} to remote {}".format(local_path, remote_path))
             
    def grab_from_remote_path(self, remote_path, local_path):
        if os.path.isdir(local_path):
            rc, output, error = self.krakken.ssh.blocking_call('basename ' + remote_path, verbose=True)
            try:
                basename = output[0]
            except IndexError:
                basename = "remote_file.txt"
            local_path += "/" + basename
        if os.path.exists(local_path):
            try:
                os.remove(local_path)
            except:
                pass 
        self.krakken.logger.info("Grabbing remote file {} and save to local {}".format(remote_path, local_path))
        try:
            self.sftp.get(remote_path, local_path)
        except Exception as e:
            self.krakken.logger.warn("Failed to get remote file {} to local {}".format(remote_path, local_path))
            self.krakken.logger.warn(str(e))
        
            