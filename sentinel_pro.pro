pro Sentinel_pro
  compile_opt IDL2
  e = envi(/headless) ; Launch the application
  ;envi, /restore_base_save_files 

  filesearch='D:\ly' ;获取根目录，这是存放所有遥感影像的文件夹
  
  ;遍历L2A的文件夹，并保存文件夹名
  files=FILE_SEARCH(filesearch,'S2*_MSIL2A*',count=num1);获取遥感影像文件夹名
  
  for i=0,num1-1 do begin
    
    ;获取待转换的JP2数据的存储路径
    jp2files=FILE_SEARCH(files[i]+'\GRANULE\','*{B02_10m.jp2,B03_10m.jp2,B04_10m.jp2,B08_10m.jp2,B05_20m.jp2,B06_20m.jp2,B07_20m.jp2}',count=jp2num)
    
    ;创建新的文件夹，用来保存处理有的数据
    file_mkdir,files[i]+'\ENVI'
    file_mkdir,files[i]+'\ENVI\temp'
    
    ;数据格式转换和选择性重采样
    for j=0,jp2num-1 do begin
      inputfile=jp2files[j]
          
      ;获取影像文件名
      inputfilesplit = Strsplit(inputfile,'\',/extract)
      outputfilename=inputfilesplit[N_ELEMENTS(inputfilesplit)-1];取打断后最后一个"\"后的字符串做输出文件名
      ;如果影像有后缀名,如.img，则需要加下面一段。若为无拓展名文件则不需要
      inputfilesplit = Strsplit(outputfilename,'.',/extract)
      outputfilename=inputfilesplit[0];取打断后最后一个"."后的字符串做输出文件名
      
      ;打开栅格图像
      raster1 = e.Openraster(inputfile) ; 读入文件
      ;影像输入指定文件夹路径：D:\ChromeDownload\..\Sentinel，转换为dat格式
      filepath_output = files[i]+'\ENVI\temp\'+outputfilename+'.dat' ; 输出文件路径
      raster1.Export, filepath_output, 'ENVI'; 输出为ENVI格式
      
      ;输出进度条
      print,FORMAT='(%"%d/%d finished!")',j+1,jp2num ;打印finished，提示完成
;      print,outputfilename
      
      ;获取图像分辨率
      inputfilesplit=Strsplit(outputfilename,'_',/extract)
      res=inputfilesplit[N_ELEMENTS(inputfilesplit)-1]
      basename=STRJOIN(inputfilesplit[0:2],'_');将"_20m"前的字符用"_"连接
;      print,res
;      print,basename

      ;若图像分辨率为20米，则重采样到10米空间分辨率
      if (res eq '20m') then BEGIN
        
        ; Get the task from the catalog of ENVITasks
        Task=ENVITask('PixelScaleResampleRaster')
        ; Define inputs
        Task.INPUT_RASTER = raster1
        Task.PIXEL_SCALE = [0.5,0.5]
        Task.OUTPUT_RASTER_URI=files[i]+'\ENVI\temp\'+basename+'_10m.dat'
        ; Run the task
        Task.Execute
      endif
      
    endfor
    
    ;波段叠加
    datfiles=FILE_SEARCH(files[i]+'\ENVI\temp\','*_10m.dat',count=datnum)
    inputfilesplit = Strsplit(datfiles[0],'\',/extract)
    outputfilename=inputfilesplit[N_ELEMENTS(inputfilesplit)-1];取打断后最后一个"\"后的字符串做输出文件名
    ;如果影像有后缀名,如.img，则需要加下面一段。若为无拓展名文件则不需要
    inputfilesplit = Strsplit(outputfilename,'_',/extract)
    ;outputfilename=inputfilesplit[0];取打断后最后一个"."后的字符串做输出文件名
    basename2=STRJOIN(inputfilesplit[0:1],'_')
;    print,basename2
    band1 = e.Openraster(datfiles[0])
    spatialRef = band1.SPATIALREF;
    
    bandNum = N_ELEMENTS(datfiles);求出波段合成顺序数组的大小
    bandArray = objarr(bandNum)
    ;按照orderArray中的顺序构造波段数组
    For k = 0,bandNum-1 do begin;
      bandArray[k] = e.Openraster(datfiles[k])
    Endfor
    
    ;开始执行波段合成操作
    Task = ENVITask("BuildBandStack")
    Task.SPATIAL_REFERENCE  = spatialRef
    Task.INPUT_RASTER = bandArray
    Task.OUTPUT_RASTER_URI = files[i]+'\ENVI\'+basename2+'_stack10m.dat'
    Task.Execute;   
    print,basename2,' Layer stacking complete!'
  endfor
  e.Close
  
  ;删除文件
  file4=FILE_SEARCH(filesearch,'S2*_MSIL2A*',count=num3);获取遥感影像文件夹名
  for i=0,num3-1 do begin
    tem_file=file4[i]+'\ENVI\temp'
    FILE_DELETE,tem_file,/RECURSIVE
  endfor
  print,'Delect_finlish'

end