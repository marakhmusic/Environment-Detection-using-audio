

from subprocess import PIPE, Popen, run



def convert_to_PCM(file, out_Fs=44100):
    cmd = ['ffmpeg', '-i', '-', '-f', 's16le', '-ar', str(out_Fs), 'pipe:1' ]
    process = Popen(cmd, stdin=file, stdout=PIPE, stderr=PIPE)
    output, error = process.communicate()
    #print(output)
    #print(error)
    return output


def save_as_wav(pcm_data, out_file='out.wav', out_Fs= 44100, output=False):
    print(f'saving pcm data as {out_file}')
    args = ['ffmpeg',
            '-y',
            '-f',
            's16le',
            '-ar',
            str(out_Fs),
            '-i',
            '-',
            out_file
            ]
    process = run(args, input=pcm_data, stderr=PIPE, stdout=PIPE)
    if output:
        print(f'process return code: {process.returncode}')
        print(process.stdout)
        print(process.stderr)
        print(f'recording  has been saved by the name of {out_file}!')


    #print('output', output)

def save_file_as_wav(file, out_name, output=True):
    print('saving file as ', out_name)
    args = ['ffmpeg',
            '-y',
            '-i', '-',
            '-ar', '44100',
            out_name]
    #process = Popen(args, stdin=file, stdout=PIPE, stderr=PIPE)

    process = run(args, stdin=file, stdout=PIPE, stderr=PIPE)
    if output:
        print(f'process return code: {process.returncode}')
        print(process.stdout)
        print(process.stderr)
        print(f'recording  has been saved by the name of {out_name}!')

    return output


def s(pcm_data, out_file='out.wav', output=True):
    print(f'saving {out_file} file')
    cmd = ['ffmpeg',
            '-y',                   # override if the file already exists
            '-f', 's16le',          # input format s16le
            "-acodec", "pcm_s16le", # raw pcm data s16 little endian input
            '-i', '-',              # pipe input
            '-ac', '1',             # mono
            out_file]              # out file name

    if output:
        print(f'cmd: {cmd}')

    process = run(cmd, input=pcm_data.tobytes(), stdout=PIPE, stderr=PIPE)
    if output:
        print(f'process return code: {process.returncode}')
        print(process.stdout)


def get_PCM(file, output=False):
    """Get the PCM data in the given file"""
    print('geting PCM data')

    args = [ 'ffmpeg',
            '-i',
            '-',
            '-f',
            's16le',
            '-ar',
            '44100',
            '-']
    process = run(args, input=file, stdout=PIPE, stderr=PIPE)
    if output:
        print(f'process return code: {process.returncode}')
        print(process.stdout)


    return process.stdout
