

def success_output_msg(msg=None):
    if not msg:
        msg = '成功'
    print('成功========================={}'.format(msg))

def error_output_msg(msg=None):
    if not msg:
        msg = '失败'
    print('失败========================={}'.format(msg))

def output_msg(msg, out=None):
    if out:
        print('output======={}================>{}'.format(out, msg))
    else:
        print('output======================={}'.format(msg))

