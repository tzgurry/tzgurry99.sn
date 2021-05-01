#coding=utf-8
import os
os.environ['MRTDATADIR']='D:/HEGTool/HEG/HEG_Win/data'
os.environ['PGSHOME']='D:/HEGTool/HEG/HEG_Win/TOOLKIT_MTD'
os.environ['MRTBINDIR']='D:/HEGTool/HEG/HEG_Win/bin'

# 设置HEG的bin路径
hegpath = 'D:/HEGTool/HEG/HEG_Win/bin'
# 指定处理模块的可执行程序文件路径，此处采用resample.exe，可以根据具体的处理问题设置
hegdo = os.path.join(hegpath, 'subset_stitch_grid.exe')
hegdo = hegdo.replace('\\', '/') # 全路径以“/”连接

year='2019'               #修改对应的年份
Total_path = '.\\2019\\' # 原始文件路径
Path_all = '.\\Index_2019\\Index_' # 将所有数据放入该文件夹下，根据年份修改
IndexArray=['NDVI','EVI','MIR reflectance','red reflectance','NIR reflectance','blue reflectance']#填入想提取的指数装入数组里
Day_Folders = os.listdir(Total_path)  # 源文件名称列表
for Indexname in IndexArray:
	Extract_Field='250m 16 days '+ Indexname    #修改提取的指数名称
	for doy in Day_Folders:
		Day_path=Total_path+doy+'\\'
		V_folder=os.listdir(Day_path)
		for v in V_folder:
			inpath=Day_path+str(v)
			if(bool(Indexname)==1):
				Indexname = Indexname.split(' ')[0]
				outpath = Path_all+Indexname+'\\Output\\'+year+'_'+doy  #输出路径
			if not os.path.exists(outpath):
				os.makedirs(outpath)
				
			# 获取当前文件夹下的所有hdf文件
			allfiles = os.listdir(inpath)
			allhdffiles = []
			for eachfile in allfiles:
				if os.path.splitext(eachfile)[1] =='.hdf':
					allhdffiles.append(eachfile)
			print('--'*20)
			print('file number:', len(allhdffiles))
			#print('  '+'\n  '.join(allhdffiles))
			print('--'*20)
			filelist=''
			k=0
			for i in allhdffiles:
				k=k+1
				if k<2: 
					temp=inpath+'\\'+i+'|'
				else:
					temp=inpath+'\\'+i
				filelist=filelist+temp    #生成输入文件名
			print(filelist)
			
			#创建Prm文件
			prmpath=Path_all+Indexname+'\\Prm\\'+year+'_'+doy
			if not os.path.exists(prmpath):
				os.makedirs(prmpath)
			t=allhdffiles[0].split('.')[0:2]
			temfname=t[0]+'_'+t[1]
			print(temfname)
			if v=='1':
				prm=['NUM_RUNS = 1\n',
					  'BEGIN\n',
					  'NUMBER_INPUTFILES = 2\n',
					  'INPUT_FILENAMES ='+filelist+'\n',
					  'OBJECT_NAME = MODIS_Grid_16DAY_250m_500m_VI|\n',
					  'FIELD_NAME = '+Extract_Field+'|\n',
					  'BAND_NUMBER = 1\n',
					  'SPATIAL_SUBSET_UL_CORNER = ( 39.999999996 57.735026912 )\n',
					  'SPATIAL_SUBSET_LR_CORNER = ( 29.999999997 91.37851024 )\n',
					  'OUTPUT_OBJECT_NAME = MODIS_Grid_16DAY_250m_500m_VI|\n',
					  'OUTGRID_X_PIXELSIZE = 0.0020833366514795377\n',
					  'OUTGRID_Y_PIXELSIZE = 0.0020833366514795377\n',
					  'RESAMPLING_TYPE = BI\n',
					  'OUTPUT_PROJECTION_TYPE = GEO\n',
					  'ELLIPSOID_CODE = WGS84\n',
					  'OUTPUT_PROJECTION_PARAMETERS = ( 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0  )\n',
					  'OUTPUT_FILENAME = '+outpath+'\\'+temfname+'_'+Indexname+'_1.tif\n',
					  'SAVE_STITCHED_FILE = NO\n',
					  'OUTPUT_STITCHED_FILENAME = '+outpath+'\\'+temfname+'_'+Indexname+'_1_stitched_.hdf\n',
					  'OUTPUT_TYPE = GEO\n'
					  'END\n']
			elif v=='2':
				prm=['NUM_RUNS = 1\n',
				  'BEGIN\n',
				  'NUMBER_INPUTFILES = 2\n',
				  'INPUT_FILENAMES ='+filelist+'\n',
				  'OBJECT_NAME = MODIS_Grid_16DAY_250m_500m_VI|\n',
				  'FIELD_NAME = '+Extract_Field+'|\n',
				  'BAND_NUMBER = 1\n',
				  'SPATIAL_SUBSET_UL_CORNER = ( 39.999999996 80.829037677 )\n',
				  'SPATIAL_SUBSET_LR_CORNER = ( 29.999999997 117.486656023 )\n',
				  'OUTPUT_OBJECT_NAME = MODIS_Grid_16DAY_250m_500m_VI|\n',
				  'OUTGRID_X_PIXELSIZE = 0.0020833366514795377\n',
				  'OUTGRID_Y_PIXELSIZE = 0.0020833366514795377\n',
				  'RESAMPLING_TYPE = BI\n',
				  'OUTPUT_PROJECTION_TYPE = GEO\n',
				  'ELLIPSOID_CODE = WGS84\n',
				  'OUTPUT_PROJECTION_PARAMETERS = ( 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0  )\n',
				  'OUTPUT_FILENAME = '+outpath+'\\'+temfname+'_'+Indexname+'_2.tif\n',
				  'SAVE_STITCHED_FILE = NO\n',
				  'OUTPUT_STITCHED_FILENAME = '+outpath+'\\'+temfname+'_'+Indexname+'_2_stitched_.hdf\n',
				  'OUTPUT_TYPE = GEO\n'
				  'END\n']
			elif v=='3':
				prm=['NUM_RUNS = 1\n',
				  'BEGIN\n',
				  'NUMBER_INPUTFILES = 2\n',
				  'INPUT_FILENAMES ='+filelist+'\n',
				  'OBJECT_NAME = MODIS_Grid_16DAY_250m_500m_VI|\n',
				  'FIELD_NAME = '+Extract_Field+'|\n',
				  'BAND_NUMBER = 1\n',
				  'SPATIAL_SUBSET_UL_CORNER = ( 29.999999997 74.492444066 )\n',
				  'SPATIAL_SUBSET_LR_CORNER = ( 19.999999998 103.923048442 )\n',
				  'OUTPUT_OBJECT_NAME = MODIS_Grid_16DAY_250m_500m_VI|\n',
				  'OUTGRID_X_PIXELSIZE = 0.0020833366514795377\n',
				  'OUTGRID_Y_PIXELSIZE = 0.0020833366514795377\n',
				  'RESAMPLING_TYPE = BI\n',
				  'OUTPUT_PROJECTION_TYPE = GEO\n',
				  'ELLIPSOID_CODE = WGS84\n',
				  'OUTPUT_PROJECTION_PARAMETERS = ( 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0  )\n',
				  'OUTPUT_FILENAME = '+outpath+'\\'+temfname+'_'+Indexname+'_3.tif\n',
				  'SAVE_STITCHED_FILE = NO\n',
				  'OUTPUT_STITCHED_FILENAME = '+outpath+'\\'+temfname+'_'+Indexname+'_3_stitched_.hdf\n',
				  'OUTPUT_TYPE = GEO\n'
				  'END\n']
							

			#生成对应的Prm,并保存
			prmfilename=prmpath +'\\'+Indexname + '_'+ str(v) +'.prm'
			print(prmfilename)
			#这里一定要注意，设定换行符为‘\n’,否则由于在windows系统下默认换行符为‘\r\n’,则无法运行成功
			fo=open(prmfilename,'w',newline='\n',encoding = 'utf-8')
			fo.writelines(prm)
			fo.close()	

			try:
				resamplefiles = '{0} -P {1}'.format(hegdo, prmfilename)
				print(resamplefiles)
				os.system(resamplefiles)        
				print(' has finished')
			except:
				# 提示错误信息
				print('was wrong')

