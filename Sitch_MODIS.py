#coding=utf-8
import os
os.environ['MRTDATADIR']='D:/HEGTool/HEG/HEG_Win/data'
os.environ['PGSHOME']='D:/HEGTool/HEG/HEG_Win/TOOLKIT_MTD'
os.environ['MRTBINDIR']='D:/HEGTool/HEG/HEG_Win/bin'

# ����HEG��bin·��
hegpath = 'D:/HEGTool/HEG/HEG_Win/bin'
# ָ������ģ��Ŀ�ִ�г����ļ�·�����˴�����resample.exe�����Ը��ݾ���Ĵ�����������
hegdo = os.path.join(hegpath, 'subset_stitch_grid.exe')
hegdo = hegdo.replace('\\', '/') # ȫ·���ԡ�/������

year='2019'               #�޸Ķ�Ӧ�����
Total_path = '.\\2019\\' # ԭʼ�ļ�·��
Path_all = '.\\Index_2019\\Index_' # ���������ݷ�����ļ����£���������޸�
IndexArray=['NDVI','EVI','MIR reflectance','red reflectance','NIR reflectance','blue reflectance']#��������ȡ��ָ��װ��������
Day_Folders = os.listdir(Total_path)  # Դ�ļ������б�
for Indexname in IndexArray:
	Extract_Field='250m 16 days '+ Indexname    #�޸���ȡ��ָ������
	for doy in Day_Folders:
		Day_path=Total_path+doy+'\\'
		V_folder=os.listdir(Day_path)
		for v in V_folder:
			inpath=Day_path+str(v)
			if(bool(Indexname)==1):
				Indexname = Indexname.split(' ')[0]
				outpath = Path_all+Indexname+'\\Output\\'+year+'_'+doy  #���·��
			if not os.path.exists(outpath):
				os.makedirs(outpath)
				
			# ��ȡ��ǰ�ļ����µ�����hdf�ļ�
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
				filelist=filelist+temp    #���������ļ���
			print(filelist)
			
			#����Prm�ļ�
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
							

			#���ɶ�Ӧ��Prm,������
			prmfilename=prmpath +'\\'+Indexname + '_'+ str(v) +'.prm'
			print(prmfilename)
			#����һ��Ҫע�⣬�趨���з�Ϊ��\n��,����������windowsϵͳ��Ĭ�ϻ��з�Ϊ��\r\n��,���޷����гɹ�
			fo=open(prmfilename,'w',newline='\n',encoding = 'utf-8')
			fo.writelines(prm)
			fo.close()	

			try:
				resamplefiles = '{0} -P {1}'.format(hegdo, prmfilename)
				print(resamplefiles)
				os.system(resamplefiles)        
				print(' has finished')
			except:
				# ��ʾ������Ϣ
				print('was wrong')

