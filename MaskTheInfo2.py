'''
该工具用于抹去患者信息，包括id，身高，体重，生日，姓名，年龄性别等
与patientId对应的id在保留的testp.txt文件中可以查到,该版本是另一版
'''
'''
edit 2018/03/16 修改，保留了患者的身高体重和性别、年龄信息
edit 2018/07/15 修改，只对患者的ID和姓名进行进行抹除，填充的为编号
'''
import os
import csv
import pydicom as pdm
import glob
import natsort
import shutil



class Config():
    pass
config=Config()
config.docEnd='.doc'
# config.ctInDir='4'
# config.ptInDir='5'
# config.ctInDir='CT_Body'
# config.ptInDir='PET_Body'
# config.ctOutDir='CT'
# config.ptOutDir='PET'
config.ctInDir='CT'
config.ptInDir='PT'
config.ctOutDir='CT'
config.ptOutDir='PT'
config.ipRoot = r'F:\0101-1122_整理（268例）'
config.opRoot = r'F:\0101-1122_脱敏（268例）'
config.beginNum=178



def maskTheInfo(inp, opRoot,indexBegin=0):
    if not os.path.exists(opRoot):
        os.mkdir(opRoot)

    patientNames = natsort.natsorted((os.listdir(inp)))
    index = indexBegin
    menu = []
    for patientFileId in patientNames:
        patientOutRootPath=os.path.join(opRoot,str(index))
        dirCtPath = os.path.join(inp, patientFileId, config.ctInDir)
        print(dirCtPath+':'+str(index))
        fileCtNames = os.listdir(dirCtPath)
        # patientDirPath = os.path.join(opRoot, str(index))
        patientDirPath = os.path.join(opRoot,str(index))
        os.mkdir(patientDirPath)
        opCtDir = os.path.join(patientOutRootPath, config.ctOutDir)
        os.mkdir(opCtDir)
        for fileCtName in fileCtNames:
            if fileCtName.startswith('CT_'):
                meta = pdm.read_file(os.path.join(dirCtPath, fileCtName))
                id = meta.PatientID
                meta.__setattr__('PatientID', str(index))
                meta.__setattr__('Accession Number', str(index))#这里也包含了患者的id
                meta.__setattr__('PatientName', str(index))

                pdm.write_file(os.path.join(opCtDir, fileCtName + '.dcm'), meta, True)

        dirPetPath = os.path.join(inp, patientFileId, config.ptInDir)
        filePetNames = os.listdir(dirPetPath)
        opPetDir = os.path.join(patientDirPath, config.ptOutDir)
        os.mkdir(opPetDir)
        for filePetName in filePetNames:
            if filePetName.startswith('PT_'):
                petmeta = pdm.read_file(os.path.join(dirPetPath, filePetName))
                pid = petmeta.PatientID
                petmeta.__setattr__('PatientID',  str(index))
                meta.__setattr__('Accession Number', str(index))  # 这里也包含了患者的id
                petmeta.__setattr__('PatientName', str(index))
                pdm.write_file(os.path.join(opPetDir, filePetName + '.dcm'), petmeta, True)

        #保存文档
        tryDoc = glob.glob(os.path.join(inp, patientFileId,'*'+config.docEnd))
        docExist = len(tryDoc) != 0
        if docExist:
            docSrcPath = tryDoc[0]
            docDesPath = os.path.join(patientDirPath, str(index) + 'report'+config.docEnd)
            shutil.copy(docSrcPath, docDesPath)

        menu.append((index, pid + '_' + patientFileId))
        index = index + 1

        writeDic(menu)

def writeDic(menu):
    pc = os.path.join(config.opRoot, 'log.txt')
    with open(pc, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(menu)

def loadDic(p):
    '''
    查看自定义id与患者id的对应关系
    :param p: csv文件存储位置
    :return: 二维数组,n*2 每行为“自定义id，患者id”
    '''
    te = []
    import csv
    with open(p, 'r') as f:
        reader = csv.reader(f)
        for lin in reader:
            if not len(lin) == 0:
                te.append(lin)
    return te


if __name__ == '__main__':


    maskTheInfo(config.ipRoot, config.opRoot,config.beginNum)
