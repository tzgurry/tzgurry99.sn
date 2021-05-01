pro modis_mosaic_cut

  compile_opt IDL2
  e = envi(/headless) ; Launch the application
  ;envi, /restore_base_save_files
  
  TotalFold='D:\MODIS\index_2019' ;获取根目录，这是存放所有指数的文件夹
  filesearch1=FILE_SEARCH(TotalFold,'Index*',count=num1) ;获取指数文件夹
  print,filesearch1
  
  for k=0,num1-1 do begin
      fileoutFolder=filesearch1[k] ; 输出文件夹
      print,'Processing'+fileoutFolder
;      print,fileoutFolder
      Dirfold=STRSPLIT(fileoutFolder,'\',/extract);获取文件夹名
      Indexname=STRSPLIT(Dirfold[-1],'_',/extract);获取指数名
      Indexname=Indexname[-1]
      print,Indexname
      ;将NDVI和EVI的忽略值设置为-3000，其它指数设置为-1000
      IgValue=-1000
      if Indexname eq 'NDVI' then begin
        IgValue=-3000
        
      endif else if Indexname eq 'EVI' then begin
        IgValue=-3000
      endif

      filesearch=filesearch1[k]+'\Output' ;获取根目录，这是存放所有遥感影像的文件夹
      fileout=filesearch1[k]
      print,filesearch
      print,fileout      

      
      ;创建新的文件夹，用来保存处理有的数据
      file_mkdir,fileout+'\Mask'
      file_mkdir,fileout+'\Cut'
      
      ;遍历MODIS的文件夹，并保存文件夹名
      foldfile=FILE_SEARCH(filesearch,'2019*',count=num);获取遥感影像文件夹名
     
     
      for i=0,num-1 do begin
          
          ; select input vector data
          vectorfile ='D:\MODIS\BJ\BJ_new.shp'
          Vector = e.OpenVector(vectorfile)
          range1=Vector.DATA_RANGE
  
          UpperLeftLat = range1[3]
  
          UpperLeftLon = range1[0]
  
          LowerRightLat = range1[1]
  
          LowerRightLon = range1[2]
          
          ;获取待镶嵌数据的存储路径
          tiffiles=FILE_SEARCH(foldfile[i],'*.tif',count=tifnum)
      
      
          inputfile=tiffiles[0]
          ;获取影像文件名
          inputfilesplit = Strsplit(inputfile,'\',/extract)
          outputfilename=inputfilesplit[N_ELEMENTS(inputfilesplit)-1];取打断后最后一个"\"后的字符串做输出文件名
          ;如果影像有后缀名,如.img，则需要加下面一段。若为无拓展名文件则不需要
          inputfilesplit = Strsplit(outputfilename,'.',/extract)
           ;取打断后最后一个"."后的字符串做输出文件名
           print,inputfilesplit[0]
          outfilename=strmid(inputfilesplit[0],0,strlen(inputfilesplit[0])-2)
          
          files=tiffiles
          
          scenes = !NULL
          FOR j=0, N_ELEMENTS(files)-1 DO BEGIN
      
            raster = e.OpenRaster(files[j])
      
            metadata = raster.METADATA
      
            ; Set the Data Ignore Value to -3000
      
            metadata.AddItem, 'data ignore value', IgValue
      
            scenes = [scenes,raster]
      
          ENDFOR
      
          ; Get the task from the catalog of ENVITasks
      
          Task = ENVITask('BuildMosaicRaster')
      
          ; Define inputs
      
          Task.INPUT_RASTERS = scenes
      
          Task.COLOR_MATCHING_METHOD = 'None'
      
      
          Task.FEATHERING_METHOD = 'None'
          Task.BACKGROUND =-3000
      
      
          ; Define outputs
          outputmask=fileout+'\Mask\'+outfilename+'.dat'
          Task.OUTPUT_RASTER_URI =outputmask
      
          ; Run the task
      
          Task.Execute
      
          print,outfilename+' msaked successful'
          
          ;裁剪
          File = outputmask
      
          Raster = e.OpenRaster(File)
          ; Get the spatial reference of the raster
      
          SpatialRef = Raster.SPATIALREF
          ; Convert from Lon/Lat to MapX/MayY
      
          SpatialRef.ConvertLonLatToMap, UpperLeftLon, UpperLeftLat, MapX, MapY
      
          SpatialRef.ConvertLonLatToMap, LowerRightLon, LowerRightLat, MapX2, MapY2
          
          Subset = ENVISubsetRaster(Raster, SPATIALREF=SpatialRef, $
      
            SUB_RECT=[MapX, MapY2, MapX2, MapY])
      
          ; Get the task from the catalog of ENVITasks
      
          Task = ENVITask('VectorMaskRaster')
      
      
          ; Define inputs
      
          Task.DATA_IGNORE_VALUE = 0
      
          Task.INPUT_MASK_VECTOR = Vector
      
          Task.INPUT_RASTER = Subset
      
      
          ; Define outputs
          outputcut=fileout+'\Cut\'+outfilename+'.dat'
          Task.OUTPUT_RASTER_URI = outputcut
      
          Task.Execute
          print,outfilename+' cut successful'
          
          
          ;释放内存

          ;获取当前内存中的所有文件的对象

          opendata = e.GetOpenData()

          ;获取数组的大小

          length1= size(opendata,/DIMENSIONS)

          for n = 0,length1[0]-1 do begin

            opendata[n].close

          endfor
          print,'~~~~~~~~~~~~~~~~free memory~~~~~~~~~~~~~~~~~~'
          
        endfor
    endfor
 end