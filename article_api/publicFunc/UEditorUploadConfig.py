
UEditorUploadSettings = {

    "imageActionName": "uploadimage", #执行上传图片的action名称 
    "imageFieldName": "file",       #提交的图片表单名称
    "imageMaxSize": 2048000,          #上传大小限制,单位B
    "imageAllowFiles": [".png", ".jpg", ".jpeg", ".gif", ".bmp"], #上传图片格式显示 
    "imageCompressEnable": True, #是否压缩图片,默认是true 
    "imageCompressBorder": 1600, #图片压缩最长边限制 
    "imageInsertAlign": None, #插入的图片浮动方式 
    "imagePath": "statics/book_img",
    "imageUrlPrefix": "http://192.168.10.207:8004",     #图片访问路径前缀
    # "imagePathFormat": "statics/zhugeleida/imgs/admin/article", #上传保存路径,可以自定义保存路径和文件名格式
    # "imagePathFormat": "C:\\Users\EDZ\PycharmProjects\zhuge\zhugeApi\statics\zhugeleida\imgs\\admin\\article", #上传保存路径,可以自定义保存路径和文件名格式


    #涂鸦图片上传配置项 
    "scrawlActionName": "uploadscrawl", #执行上传涂鸦的action名称 
    "scrawlFieldName": "upfile", #提交的图片表单名称 
    "scrawlPathFormat": "upfiles/{user_dir}/{filename}.{extname}", #上传保存路径,可以自定义保存路径和文件名格式 
    "scrawlMaxSize": 2048000, #上传大小限制,单位B 
    "scrawlUrlPrefix": "",    #图片访问路径前缀
    "scrawlInsertAlign": None,

    #截图工具上传 
    "snapscreenActionName": "uploadimag", #执行上传截图的action名称
    "snapscreenPathFormat": "upfiles/{user_dir}/{filename}.{extname}", #上传保存路径,可以自定义保存路径和文件名格式 
    "snapscreenUrlPrefix": "", #图片访问路径前缀 
    "snapscreenInsertAlign": None, #插入的图片浮动方式 

    #抓取远程图片配置 
    "catcherLocalDomain": ["127.0.0.1", "localhost", "img.baidu.com"],
    "catcherActionName": "catchimage", #执行抓取远程图片的action名称 
    "catcherFieldName": "source", #提交的图片列表表单名称 
    "catcherPathFormat": "upfiles/{user_dir}/{filename}.{extname}", #上传保存路径,可以自定义保存路径和文件名格式 
    "catcherUrlPrefix": "", #图片访问路径前缀 
    "catcherMaxSize": 2048000, #上传大小限制,单位B 
    "catcherAllowFiles": [".png", ".jpg", ".jpeg", ".gif", ".bmp"], #抓取图片格式显示 

    #上传视频配置 
    "videoActionName": "uploadvideo", #执行上传视频的action名称 
    "videoFieldName": "upfile", #提交的视频表单名称 
    "videoPathFormat": "upfiles/{user_dir}/{filename}.{extname}", #上传保存路径,可以自定义保存路径和文件名格式 
    "videoUrlPrefix": "", #视频访问路径前缀 
    "videoMaxSize": 102400000, #上传大小限制,单位B,默认100MB 
    "videoAllowFiles": [
        ".flv", ".swf", ".mkv", ".avi", ".rm", ".rmvb", ".mpeg", ".mpg",
        ".ogg", ".ogv", ".mov", ".wmv", ".mp4", ".webm", ".mp3", ".wav", ".mid"], #上传视频格式显示 

    #上传文件配置 
    "fileActionName": "uploadfile", #controller里,执行上传视频的action名称 
    "fileFieldName": "upfile", #提交的文件表单名称 
    "filePathFormat": "upfiles/{user_dir}/{filename}.{extname}", #上传保存路径,可以自定义保存路径和文件名格式 
    "fileUrlPrefix": "", #文件访问路径前缀 
    "fileMaxSize": 51200000, #上传大小限制,单位B,默认50MB 
    "fileAllowFiles": [
        ".png", ".jpg", ".jpeg", ".gif", ".bmp",
        ".flv", ".swf", ".mkv", ".avi", ".rm", ".rmvb", ".mpeg", ".mpg",
        ".ogg", ".ogv", ".mov", ".wmv", ".mp4", ".webm", ".mp3", ".wav", ".mid",
        ".rar", ".zip", ".tar", ".gz", ".7z", ".bz2", ".cab", ".iso",
        ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".pdf", ".txt", ".md", ".xml"
    ], #上传文件格式显示 

    #列出指定目录下的图片 
    "imageManagerActionName": "listimage", #执行图片管理的action名称 
    "imageManagerListPath": "upfiles/{user_dir}/", #指定要列出图片的目录 
    "imageManagerListSize": 20, #每次列出文件数量 
    "imageManagerUrlPrefix": "", #图片访问路径前缀 
    "imageManagerInsertAlign": None, #插入的图片浮动方式 
    "imageManagerAllowFiles": [".png", ".jpg", ".jpeg", ".gif", ".bmp"], #列出的文件类型 

    #列出指定目录下的文件 
    "fileManagerActionName": "listfile", #执行文件管理的action名称 
    "fileManagerListPath": "upfiles/{user_dir}/", #指定要列出文件的目录 
    "fileManagerUrlPrefix": "", #文件访问路径前缀 
    "fileManagerListSize": 20, #每次列出文件数量 
    "fileManagerAllowFiles": [
        ".png", ".jpg", ".jpeg", ".gif", ".bmp",
        ".flv", ".swf", ".mkv", ".avi", ".rm", ".rmvb", ".mpeg", ".mpg",
        ".ogg", ".ogv", ".mov", ".wmv", ".mp4", ".webm", ".mp3", ".wav", ".mid",
        ".rar", ".zip", ".tar", ".gz", ".7z", ".bz2", ".cab", ".iso",
        ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".pdf", ".txt", ".md", ".xml"
    ] #列出的文件类型 
}
