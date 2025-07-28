# Bilibili缓存转换器

将Bilibili的缓存文件转换为MP4格式的GUI工具。

## 测试环境

- Bilibili客户端PC版1.16.5
- Windows 10

## 安装使用

### Python环境运行
1. 安装Python 3.6+

2. 安装ffmpeg:
   - Windows: 
     - 下载并安装 [ffmpeg](https://ffmpeg.org/download.html)
     - 配置环境变量:
       1. 找到ffmpeg安装目录下的bin文件夹(如C:\ffmpeg\bin)
       2. 右键"此电脑" → "属性" → "高级系统设置" → "环境变量"
       3. 在"系统变量"中找到Path变量 → 点击"编辑"
       4. 点击"新建" → 粘贴ffmpeg的bin目录路径 → 点击"确定"
       5. 验证安装: 打开cmd输入`ffmpeg -version`，应显示版本信息

3. 安装依赖:
   ```
   pip install -r requirements.txt
   ```
   依赖包:
   - pyinstaller==5.13.2
   - ffmpeg-python==0.2.0

4. 运行程序:
   ```
   python bilibili_converter.py
   ```

### 打包为EXE使用

1. 确保已安装Python和ffmpeg
2. 安装打包工具:
   ```
   pip install -r requirements.txt
   ```
3. 执行打包命令:
   ```
   pyinstaller --onefile --windowed bilibili_converter.py
   ```
4. 打包完成后，在dist目录中找到BilibiliConverter.exe
5. 直接双击运行即可

## 使用方法
1. 选择Bilibili缓存目录
2. 选择输出目录
3. 点击"开始转换"按钮
