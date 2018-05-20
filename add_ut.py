# coding:utf-8
import os
import sys
import bencoder
import hashlib
import time
import shutil
import binascii

def get_torrent_file_name(rootDir):
    L = [];
    for root, dirs, files in os.walk(rootDir):
        for file in files:
            if os.path.splitext(file)[1] == '.torrent':
                L.append(os.path.join(root, file))
    return L;

root_dir = sys.argv[1];
utorrent_dir = sys.argv[2];
#root_dir = "I:\Ruby"
#utorrent_dir = "I:\Ruby"

all_torrent_file_full_name = get_torrent_file_name(root_dir)
'''
for torrent_file_name in all_torrent_file_full_name:
    print(torrent_file_name)'''
print('一共有%d个种子文件' % len(all_torrent_file_full_name));

''''
test = '123';
fuck = bencoder.encode(test);
f = open(torrentName , "rb")
d = bencoder.decode(f.read())
f.close();
'''

# 读取resume.dat文件
resume_file_name = utorrent_dir + str(os.sep) + r'resume.dat'
resume_file = open(resume_file_name, 'rb')
# test = resume_file.read();
metadata = bencoder.decode(resume_file.read())
resume_file.close();

# 备份resume.dat文件
resume_bak_file_name = resume_file_name + r'-' + time.strftime('%Y%m%d-%H%M%S',time.localtime(time.time()))
if not (os.path.exists(resume_bak_file_name)):
    shutil.copyfile(resume_file_name, resume_bak_file_name)

# 取所有种子的Hash值记录
del metadata[b'.fileguard'];
del metadata[b'rec'];
torrent_file_list = metadata.keys();
torrent_hash_list = []
for key, value in metadata.items():
    if not(isinstance(value, dict)):
        '''
            # 异常记录'''
        continue;
    torrent_hash_list.append(value[b'info'])

# 逐一根据torrent文件修改resume.dat数据
for torrent_file_full_name in all_torrent_file_full_name:
    torrent_file_name = str.encode(os.path.basename(torrent_file_full_name));
    torrent_file_path = str.encode(os.path.dirname(torrent_file_full_name));

    with open(torrent_file_full_name, 'rb') as torrentfile:
        torrent_file = bencoder.decode(torrentfile.read())
        torrent_info = torrent_file[b'info'];
        hashcontents = bencoder.encode(torrent_info)
        digest = hashlib.sha1(hashcontents).digest()
        '''
        fuck1 = hashlib.sha1(hashcontents).hexdigest();
        fuck2 = binascii.hexlify(digest);
        fuck3 = binascii.unhexlify(fuck1);
        fuck4 = binascii.hexlify(fuck3);
        fuck5 = str.encode(fuck1);
        fuck6 = bytes.decode(fuck5);
        '''

        if digest in torrent_hash_list:     # 查重
            '''
                # 重复值记录'''
            continue
        metadata[torrent_file_name] = {};
        metadata[torrent_file_name][b'info'] = digest;
        metadata[torrent_file_name][b'caption'] = torrent_file_path.split(str.encode(os.sep))[-1];
        if b'files' in torrent_file[b'info']:       # 多文件
            metadata[torrent_file_name][b'path'] = torrent_file_path;
            # print("Multi File");
        elif b'length' in torrent_file[b'info']:    # 单文件
            content_file_name = torrent_info[b'name'];
            metadata[torrent_file_name][b'path'] = torrent_file_path + str.encode(os.sep) + content_file_name;
            # print("Single File");
        '''
        else:
            # 异常记录'''

    # 复制torrent文件
    torrent_dir_name = utorrent_dir + os.sep + r'Torrents' + os.sep + time.strftime('%Y%m%d-%H%M%S',time.localtime(time.time()))
    if not(os.path.exists(torrent_dir_name)):
        os.makedirs(torrent_dir_name)
    torrent_new_full_name = torrent_dir_name + os.sep + os.path.split(torrent_file_full_name)[1]
    if not(os.path.exists(torrent_new_full_name)):
        shutil.copyfile(torrent_file_full_name, torrent_new_full_name)
    '''else:
        记录重名种子文件
    '''


# 保存resume.dat文件
resume_file = open(resume_file_name+'-', 'wb');
resume_file.write(bencoder.encode(metadata));
resume_file.close();

pass
