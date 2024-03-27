import xml.etree.ElementTree as ET
import re
from gen_path import edge2graph, run
import networkx as nx
import matplotlib.pyplot as plt


def getType(str_type_list, rst_list):
    # 去除空格
    for str_type in str_type_list:
        if str_type == '':
            continue
        str_type = str_type.replace(' ', '')
        rst = re.findall('\\<(.*)>', str_type)
        if rst.__len__() == 0:
            rst_list.append(str_type)
        else:
            # 先切分逗号
            tmp_list = rst[0].split(',')
            if '<' in tmp_list[0]:
                tmp = [','.join(tmp_list[:-1]), tmp_list[-1]]
            else:
                tmp = [tmp_list[0], ','.join(tmp_list[1:])]
            getType(tmp, rst_list)


def getPreType(str_type_list, rst_list):
    # 去除空格
    for str_type in str_type_list:
        if str_type == '':
            continue
        str_type = str_type.replace(' ', '')
        pre = re.findall('(.*)<', str_type)
        if pre.__len__() == 0:
            rst_list.append(str_type)
        else:
            # 先切分逗号
            tmp_list = pre[0].split(',')
            if '<' in tmp_list[0]:
                tmp = [','.join(tmp_list[:-1]), tmp_list[-1]]
            else:
                tmp = [tmp_list[0], ','.join(tmp_list[1:])]
            getPreType(tmp, rst_list)

# 解析成树


def xmlAnalyse(xml_path):
    fileName = xml_path
    tree = ET.parse(fileName)
    root = tree.getroot()
    ns = dict([node for _, node in ET.iterparse(fileName, events=['start-ns'])])
    for key in ns:
        ET.register_namespace(key, ns[key])
    # 查找包
    classViewNode = root.find("*/packagedElement/packagedElement[@name='Class View']")
    sequenceViewNode = root.find("*/packagedElement/packagedElement[@name='Sequence View']")
    useCaseNode = root.find("*/packagedElement/packagedElement[@name='Use Case']")
    activeViewNode = root.find("*/packagedElement/packagedElement[@name='Active View']")
    componentViewNode = root.find("*/packagedElement/packagedElement[@name='Component View']")
    deploymentViewNode = root.find("*/packagedElement/packagedElement[@name='Deployment View']")

    indexDict = {}
    # 查找类节点
    classNodeList = classViewNode.findall('.//packagedElement')
    classNodeDict = {}
    interfaceNodeDict = {}

    relationSet = set()

    operationMap = {}
    # autoInterfaceSet = set()
    autoInterfaceDict = {}
    # autoClassSet = set()
    autoClassDict = {}
    autoRelationSet = set()
    autoImplClass = {}

    operationDict = {}
    messages = set()
    # 类名：{'id'=[], 'visibility':private, 'static':false, 'final':false, 'abstract':false, 'attrs':[(权限, 修饰符, 类型, 变量名, 初始值), ... ], 'methods':[(权限, 修饰符, 返回值类型, 方法名, 参数列表[(类型, 参数名)]), ... ]}
    for cn in classNodeList:
        if cn.get('{' + ns['xmi'] + '}type') == 'uml:Class':
            classNodeDict[cn.get('{' + ns['xmi'] + '}id')] = {'name': cn.attrib['name']}
            indexDict[cn.get('{' + ns['xmi'] + '}id')] = {'name': cn.attrib['name'], 'type': 'Class'}
        elif cn.get('{' + ns['xmi'] + '}type') == 'uml:Interface':
            interfaceNodeDict[cn.get('{' + ns['xmi'] + '}id')] = {'name': cn.attrib['name']}
            indexDict[cn.get('{' + ns['xmi'] + '}id')] = {'name': cn.attrib['name'], 'type': 'Class'}
        else:
            continue
    classSet = set()
    for key in classNodeDict.keys():
        if classNodeDict[key]['name'] in classSet:
            raise Exception("出现同名类")
        else:
            classSet.add(classNodeDict[key]['name'])
    interfaceSet = set()
    for key in interfaceNodeDict.keys():
        if interfaceNodeDict[key]['name'] in interfaceSet:
            raise Exception('出现同名接口')
        else:
            interfaceSet.add(interfaceNodeDict[key]['name'])

    # 查询类节点成员变量和成员函数
    for key in classNodeDict.keys():
        elementNode = root.find('*/elements/element[@xmi:idref="'+key+'"]', ns)
        if elementNode is None:
            raise Exception(key+"元素无法找到")
        # 找到属性节点
        propNode = elementNode.find('./properties', ns)
        if propNode is None:
            raise Exception(key+"无属性节点")
        classNodeDict[key]['visibility'] = propNode.attrib['scope']
        # 静态修饰
        if propNode.get('isStatic') == "true":
            classNodeDict[key]['static'] = "true"
        else:
            classNodeDict[key]['static'] = "false"
        # 抽象修饰
        if propNode.get('isAbstract') == "true":
            classNodeDict[key]['abstract'] = "true"
        else:
            classNodeDict[key]['abstract'] = "false"
        # final修饰
        if propNode.get('changeability') is not None and propNode.get('changeability') != "changeable":
            classNodeDict[key]['final'] = "true"
        else:
            classNodeDict[key]['final'] = "false"
        autoClassNode = propNode.get('genlinks')
        if autoClassNode is not None:
            autoList = autoClassNode.split(";")
            for al in autoList:
                al_tmp = al.split('=')
                if len(al_tmp) == 2:
                    # al_tmp[0]为关系 al_tmp[1]为补全
                    # 类, 实现, 接口
                    if al_tmp[0].lower() == "realization" or al_tmp[0].lower() == 'implements':
                        autoRelationSet.add((classNodeDict[key]['name'], key, 'Realization', al_tmp[1], key+'Auto'+al_tmp[1]))
                        indexDict[key + 'Auto'+al_tmp[1]] = {'name': al_tmp[1], 'type': 'Auto'}
                        weight = ((len(al_tmp[1]) + 2) / 10.0 + 1) / 10.0
                        operationDict[al_tmp[1]] = {'*type': 'Auto', 'Dangerous Calls': weight, al_tmp[1]+'()': weight}
                        # autoInterfaceSet.add(al_tmp[1])
                        autoInterfaceDict[key+'Auto'+al_tmp[1]] = {'name': al_tmp[1]}
                        messages.add((al_tmp[1], 'Dangerous Calls', classNodeDict[key]['name']))
                    # 子类, 泛化, 父类
                    elif al_tmp[0].lower() == "generalization" or al_tmp[0].lower() == 'extends' or al_tmp[0].lower() == 'parent':
                        autoRelationSet.add((classNodeDict[key]['name'], key, 'Generalization', al_tmp[1], key+'Auto'+al_tmp[1]))
                        indexDict[key + 'Auto'+al_tmp[1]] = {'name': al_tmp[1], 'type': 'Auto'}
                        weight = ((len(al_tmp[1]) + 2) / 10.0 + 1) / 10.0
                        operationDict[al_tmp[1]] = {'*type': 'Auto', 'Dangerous Calls': weight, al_tmp[1]+'()': weight}
                        # autoClassSet.add(al_tmp[1])
                        autoClassDict[key+'Auto'+al_tmp[1]] = {'name': al_tmp[1]}
                        messages.add((al_tmp[1], 'Dangerous Calls', classNodeDict[key]['name']))
                    else:
                        autoRelationSet.add((classNodeDict[key]['name'], key, al_tmp[0], al_tmp[1], key+'Auto'+al_tmp[1]))
                        indexDict[key + 'Auto'+al_tmp[1]] = {'name': al_tmp[1], 'type': 'Auto'}
                        weight = ((len(al_tmp[1]) + 2) / 10.0 + 1) / 10.0
                        operationDict[al_tmp[1]] = {'*type': 'Auto', 'Dangerous Calls': weight, al_tmp[1]+'()': weight}
                        # autoClassSet.add(al_tmp[1])
                        autoClassDict[key + 'Auto'+al_tmp[1]] = {'name': al_tmp[1]}
                        messages.add((al_tmp[1], 'Dangerous Calls', classNodeDict[key]['name']))
        # 查找成员变量
        # 'attrs':[(权限, 修饰符, 类型, 变量名, 初始值), ... ]
        attrNodeList = elementNode.findall("./attributes/attribute", ns)
        attrs = []
        for attr in attrNodeList:
            attrScope = attr.get('scope')
            attrPropNode = attr.find("./properties")
            attrStatic = attrPropNode.get('static')
            propList = []
            if attrStatic == "1":
                propList.append('static')
            attrFinal = attrPropNode.get('changeability')
            if attrFinal == "frozen":
                propList.append('final')
            attrType = attrPropNode.get('type')
            attrName = attr.get('name')
            attrInit = attr.find('./initial').get('body')
            if attrInit is None:
                attrInit = "None"
            attrs.append([attrScope, propList, attrType, attrName, attrInit])
        classNodeDict[key]['attrs'] = attrs
        operationDict[classNodeDict[key]['name']] = {'*type': 'Class'}
        # 查找成员函数
        # 'methods':[(权限, 修饰符, 返回值类型, 方法名, 参数列表[(类型, 参数名)]), ... ]
        methodNodeList = elementNode.findall('./operations/operation', ns)
        methods = []
        for met in methodNodeList:
            # 对每个方法赋予权值
            weight = 0.0
            all_split = []
            # 权限
            metScope = met.get('scope')
            if metScope.lower() == 'public':
                weight += 1.0
            elif metScope.lower() == 'protected':
                weight += 2.0
            else:
                weight += 4.0
            # 修饰符
            metTypeNode = met.find('./type', ns)
            propList = []
            metStatic = metTypeNode.get('static')
            metConst = metTypeNode.get('const')
            metAbstract = metTypeNode.get('isAbstract')
            metSynchronised = metTypeNode.get('synchronised')
            if metConst != "false":
                propList.append('const')
                weight += 1.0
            if metStatic != "false":
                propList.append('static')
                weight += 1.0
            if metAbstract != "false":
                propList.append('abstract')
                weight += 1.0
            if metSynchronised == "1":
                propList.append('synchronised')
                weight += 1.0
            # 返回值类型
            metReturn = metTypeNode.get('type')
            if metReturn is not None:
                # 构造函数没有返回值
                if metReturn.lower() != 'void':
                    all_split.append(metReturn)
            # 方法名
            metName = met.get('name')
            # 参数列表
            paraList = []
            paraNodeList = met.findall('./parameters/parameter', ns)
            for para in paraNodeList:
                paraID = para.get('{' + ns['xmi'] + '}idref')
                paraNode = classViewNode.find('.//ownedOperation/ownedParameter[@xmi:id="'+paraID+'"]', ns)
                if paraNode is not None:
                    if paraNode.attrib['direction'] != 'return':
                        paraName = paraNode.get('name')
                        paraProp = para.find('./properties', ns)
                        paraPos = int(paraProp.get('pos'))
                        paraType = paraProp.get('type')
                        paraList.append([paraPos, paraType, paraName])
                        all_split.append(paraType)
            paraList.sort()
            tmp = [(p[1], p[2]) for p in paraList]
            methods.append([metScope, propList, metReturn, metName, tmp])
            typeTmp = ", ".join([p[1] for p in paraList])
            operationTmp = metName+'('+typeTmp+')'
            metId = met.get('{' + ns['xmi'] + '}idref')
            # 从packagedElement/node读取的是operation的idref
            ea_guid = met.find('./tags/tag[@name="ea_guid"]', ns)
            if metId is not None:
                operationMap[metId] = {'ea_guid': ea_guid, 'parentType': 'Class', 'parent': classNodeDict[key]['name'], 'operation': operationTmp, 'frequency': 0}
            typeList = []
            for tmpSplitType in all_split:
                if '<' in tmpSplitType:
                    getPreType([tmpSplitType], typeList)
                    getType([tmpSplitType], typeList)
                else:
                    typeList.append(tmpSplitType)
            weight += len(typeList)
            # 防御系数
            # defense_weight = random.randint(0, 10)
            # 保证实验可重复性
            defense_weight = len(operationTmp) / 10
            weight += defense_weight
            operationDict[classNodeDict[key]['name']][operationTmp] = (weight / 10)
        classNodeDict[key]['methods'] = methods
        weight = (len(classNodeDict[key]['name']) + 2) / 10 + 1  # 构造函数的可见性为public
        operationDict[classNodeDict[key]['name']][classNodeDict[key]['name'] + '()'] = (weight / 10)
        # 类节点关系
        linkNode = elementNode.find('./links', ns)
        if linkNode is not None:
            for relationNode in linkNode.iter():
                relation_tmp = relationNode.tag
                if relation_tmp != 'links':
                    startClass = indexDict[relationNode.attrib['start']]['name']
                    endClass = indexDict[relationNode.attrib['end']]['name']
                    relationSet.add((startClass, relationNode.attrib['start'], relation_tmp, endClass, relationNode.attrib['end']))

    # 接口处理
    for key in interfaceNodeDict.keys():
        elementNode = root.find('*/elements/element[@xmi:idref="' + key + '"]', ns)
        if elementNode is None:
            raise Exception(key + "元素无法找到")
        # 找到属性节点
        propNode = elementNode.find('./properties', ns)
        if propNode is None:
            raise Exception(key+"无属性节点")
        interfaceNodeDict[key]['visibility'] = propNode.attrib['scope']
        # 静态修饰
        if propNode.get('isStatic') == "true":
            interfaceNodeDict[key]['static'] = "true"
        else:
            interfaceNodeDict[key]['static'] = "false"
        # 抽象修饰
        if propNode.get('isAbstract') == "true":
            interfaceNodeDict[key]['abstract'] = "true"
        else:
            interfaceNodeDict[key]['abstract'] = "false"
        # final修饰
        if propNode.get('changeability') is not None and propNode.get('changeability') != "changeable":
            interfaceNodeDict[key]['final'] = "true"
        else:
            interfaceNodeDict[key]['final'] = "false"
        # 查找成员变量
        # 'attrs':[(权限, 修饰符, 类型, 变量名, 初始值), ... ]
        attrNodeList = elementNode.findall("./attributes/attribute", ns)
        attrs = []
        for attr in attrNodeList:
            attrScope = attr.get('scope')
            attrPropNode = attr.find("./properties")
            attrStatic = attrPropNode.get('static')
            propList = []
            if attrStatic == "1":
                propList.append('static')
            attrFinal = attrPropNode.get('changeability')
            if attrFinal == "frozen":
                propList.append('final')
            attrType = attrPropNode.get('type')
            attrName = attr.get('name')
            attrInit = attr.find('./initial').get('body')
            if attrInit is None:
                attrInit = "None"
            attrs.append([attrScope, propList, attrType, attrName, attrInit])
        interfaceNodeDict[key]['attrs'] = attrs
        operationDict[interfaceNodeDict[key]['name']] = {'*type': 'Interface'}
        # 查找成员函数
        # 'methods':[(权限, 修饰符, 返回值类型, 方法名, 参数列表[(类型, 参数名)]), ... ]
        methodNodeList = elementNode.findall('./operations/operation', ns)
        methods = []
        for met in methodNodeList:
            # 对每个方法赋予权值
            weight = 0.0
            all_split = []
            # 权限
            metScope = met.get('scope')
            if metScope.lower() == 'public':
                weight += 1.0
            elif metScope.lower() == 'protected':
                weight += 2.0
            else:
                weight += 4.0
            # 修饰符
            metTypeNode = met.find('./type', ns)
            propList = []
            metStatic = metTypeNode.get('static')
            metConst = metTypeNode.get('const')
            metAbstract = metTypeNode.get('isAbstract')
            metSynchronised = metTypeNode.get('synchronised')
            if metConst != "false":
                propList.append('const')
                weight += 1.0
            if metStatic != "false":
                propList.append('static')
                weight += 1.0
            if metAbstract != "false":
                propList.append('abstract')
                weight += 1.0
            if metSynchronised == "1":
                propList.append('synchronised')
                weight += 1.0
            # 返回值类型
            metReturn = metTypeNode.get('type')
            if metReturn is not None:
                # 构造函数没有返回值
                if metReturn.lower() != 'void':
                    all_split.append(metReturn)
            # 方法名
            metName = met.get('name')
            # 参数列表
            paraList = []
            paraNodeList = met.findall('./parameters/parameter', ns)
            for para in paraNodeList:
                paraID = para.get('{' + ns['xmi'] + '}idref')
                paraNode = classViewNode.find('.//ownedOperation/ownedParameter[@xmi:id="' + paraID + '"]', ns)
                if paraNode is not None:
                    if paraNode.attrib['direction'] != 'return':
                        paraName = paraNode.get('name')
                        paraProp = para.find('./properties', ns)
                        paraPos = int(paraProp.get('pos'))
                        paraType = paraProp.get('type')
                        paraList.append([paraPos, paraType, paraName])
                        all_split.append(paraType)
            paraList.sort()
            tmp = [(p[1], p[2]) for p in paraList]
            methods.append([metScope, propList, metReturn, metName, tmp])

            typeTmp = ", ".join([p[1] for p in paraList])
            operationTmp = metName + '(' + typeTmp + ')'
            metId = met.get('{' + ns['xmi'] + '}idref')
            # 从packagedElement/node读取的是operation的idref
            ea_guid = met.find('./tags/tag[@name="ea_guid"]', ns)
            if metId is not None:
                operationMap[metId] = {'ea_guid': ea_guid, 'parentType': 'Interface', 'parent': interfaceNodeDict[key]['name'], 'operation': operationTmp, 'frequency': 0}
            # if tagNode is not None:
            #     operationMap[tagNode.attrib['value']] = {'id': tagNode.get('{' + ns['xmi'] + '}id'), 'type': 'Interface', 'Interface': interfaceNodeDict[key]['name'], 'operation': operationTmp, 'frequency': 0}
            typeList = []
            for tmpSplitType in all_split:
                if '<' in tmpSplitType:
                    getPreType([tmpSplitType], typeList)
                    getType([tmpSplitType], typeList)
                else:
                    typeList.append(tmpSplitType)
            weight += len(typeList)
            # 防御系数
            # defense_weight = random.randint(0, 10)
            # weight += defense_weight
            defense_weight = len(operationTmp) / 10
            weight += defense_weight
            operationDict[interfaceNodeDict[key]['name']][operationTmp] = (weight / 10)
        interfaceNodeDict[key]['methods'] = methods
        weight = (len(interfaceNodeDict[key]['name'])+2) / 10 + 1  # 构造函数的权限为public
        operationDict[interfaceNodeDict[key]['name']][interfaceNodeDict[key]['name']+'()'] = (weight / 10)
        # 接口没有实现类在links中没有Realisation
        linkNode = elementNode.find('./links', ns)
        tagSet = set()
        if linkNode is not None:
            for relationNode in linkNode.iter():
                relation_tmp = relationNode.tag
                if relation_tmp != 'links':
                    tagSet.add(relation_tmp)
                    startInterface = indexDict[relationNode.attrib['start']]['name']
                    endInterface = indexDict[relationNode.attrib['end']]['name']
                    relationSet.add((startInterface, relationNode.attrib['start'], relation_tmp, endInterface, relationNode.attrib['end']))
        # if "Realisation" not in tagSet:
        #     implKey = key + 'Impl'
        #     autoImplClass[implKey] = {}
        #     indexDict[implKey] = {'name': interfaceNodeDict[key]['name'] + 'Impl', 'type': 'Class'}
        #     autoImplClass[implKey]['name'] = interfaceNodeDict[key]['name'] + 'Impl'
        #     autoImplClass[implKey]['visibility'] = interfaceNodeDict[key]['visibility']
        #     autoImplClass[implKey]['static'] = interfaceNodeDict[key]['static']
        #     autoImplClass[implKey]['abstract'] = 'false'
        #     autoImplClass[implKey]['final'] = interfaceNodeDict[key]['final']
        #     autoImplClass[implKey]['attrs'] = copy.deepcopy(interfaceNodeDict[key]['attrs'])
        #     autoImplClass[implKey]['methods'] = copy.deepcopy(interfaceNodeDict[key]['methods'])
        #     for met in autoImplClass[implKey]['methods']:
        #         if 'abstract' in met[1]:
        #             met[1].remove('abstract')
        #     autoRelationSet.add((autoImplClass[implKey]['name'], implKey, 'Realisation', interfaceNodeDict[key]['name'], key))

    reverseClassDict = {}
    for key in indexDict.keys():
        cName = indexDict[key]['name']
        reverseClassDict[cName] = {}
        reverseClassDict[cName]['id'] = key
        reverseClassDict[cName]['type'] = indexDict[key]['type']

    # 处理组件节点
    componentNodeList = componentViewNode.findall('.//packagedElement', ns)
    componentDict = {}
    componentRelationSet = set()

    for com in componentNodeList:
        if com.get('{' + ns['xmi'] + '}type') == 'uml:Component':
            componentDict[com.get('{' + ns['xmi'] + '}id')] = {'name': com.attrib['name']}
            indexDict[com.get('{' + ns['xmi'] + '}id')] = {'name': com.attrib['name'], 'type': 'Component'}
        else:
            continue
    reverseComponentDict = {}
    componentSet = set()
    for key in componentDict.keys():
        cName = componentDict[key]['name']
        if cName in componentSet:
            raise Exception('组件重名')
        else:
            componentSet.add(cName)
            reverseComponentDict[cName] = {'id': key, 'type': 'Component'}

    classNameList = list(reverseClassDict.keys())
    for key in componentDict.keys():
        elementNode = root.find('*/elements/element[@xmi:idref="' + key + '"]', ns)
        if elementNode is None:
            raise Exception(key + "元素无法找到")
        # 找到属性节点
        propNode = elementNode.find('./properties', ns)
        if propNode is None:
            raise Exception(key + "无属性节点")
        componentDict[key]['visibility'] = propNode.attrib['scope']
        # 静态修饰
        if propNode.get('isStatic') == "true":
            componentDict[key]['static'] = "true"
        else:
            componentDict[key]['static'] = "false"
        # 抽象修饰
        if propNode.get('isAbstract') == "true":
            componentDict[key]['abstract'] = "true"
        else:
            componentDict[key]['abstract'] = "false"
        # final修饰
        if propNode.get('changeability') is not None and propNode.get('changeability') != "changeable":
            componentDict[key]['final'] = "true"
        else:
            componentDict[key]['final'] = "false"
        # 查找组件包含的类成员
        # 'attrs':[[权限, 修饰符, 类型, 变量名], ... ]
        attrNodeList = elementNode.findall("./attributes/attribute", ns)
        attrs = []
        for attr in attrNodeList:
            attrScope = attr.get('scope')
            attrPropNode = attr.find("./properties")
            attrStatic = attrPropNode.get('static')
            propList = []
            if attrStatic == "1":
                propList.append('static')
            attrFinal = attrPropNode.get('changeability')
            if attrFinal == "frozen":
                propList.append('final')
            attrType = attrPropNode.get('type')
            attrName = attr.get('name')
            attrs.append([attrScope, propList, attrType, attrName])
            if attrType not in classNameList:
                autoClassDict[key+'Auto' + attrType] = {'name': attrType}
                classNameList.append(attrType)
                weight = ((len(attrType) + 2) / 10.0 + 1) / 10.0
                operationDict[attrType] = {'*type': 'Auto', 'Dangerous Calls': weight, attrType+'()': weight}
                indexDict[key+'Auto' + attrType] = {'name': attrType, 'type': 'Auto'}
                reverseClassDict[attrType] = {'id': key+'Auto'+attrType, 'type': 'Auto'}
            componentRelationSet.add((componentDict[key]['name'], key, 'Component Contain', attrType, reverseClassDict[attrType]['id']))
        componentDict[key]['attrs'] = attrs
        # 组件间关系
        linkNode = elementNode.find('./links', ns)
        if linkNode is not None:
            for relationNode in linkNode.iter():
                relation_tmp = relationNode.tag
                if relation_tmp != 'links':
                    startComponent = indexDict[relationNode.attrib['start']]['name']
                    endComponent = indexDict[relationNode.attrib['end']]['name']
                    componentRelationSet.add((startComponent, relationNode.attrib['start'], relation_tmp, endComponent, relationNode.attrib['end']))
                    if relation_tmp == 'Association':
                        componentRelationSet.add((endComponent, relationNode.attrib['end'], relation_tmp, startComponent, relationNode.attrib['start']))

    autoClassSet = set()
    autoInterfaceSet = set()
    for key in autoClassDict.keys():
        autoClassSet.add(autoClassDict[key]['name'])

    for key in autoInterfaceDict.keys():
        autoInterfaceSet.add(autoInterfaceDict[key]['name'])
    # 补全类间关系和实体识别
    entityClass = {}
    for key in classNodeDict:
        # 补全类间关系
        attrs = classNodeDict[key]['attrs']
        tmp_type_list = []
        for attr in attrs:
            # 获取<>之间的数据类型
            attrType = attr[2]
            getType([attrType], tmp_type_list)
            getPreType([attrType], tmp_type_list)
        mets = classNodeDict[key]['methods']
        for met in mets:
            paraList = [i[0] for i in met[-1]]
            getType(paraList, tmp_type_list)
            getPreType(paraList, tmp_type_list)
        tmp_type_list = set(tmp_type_list)
        for at in tmp_type_list:
            if at in classSet:
                if indexDict[key]['name'] != at:
                    relationSet.add((indexDict[key]['name'], key, 'Association', at, reverseClassDict[at]['id']))
            elif at in interfaceSet:
                if indexDict[key]['name'] != at:
                    relationSet.add((indexDict[key]['name'], key, 'Association', at, reverseClassDict[at]['id']))
                # relationSet.add((indexDict[key]['name'], key, 'Association', attr[2] + 'Impl', reverseClassDict[attr[2] + 'Impl']['id']))
            elif at in autoClassSet:
                if indexDict[key]['name'] != at:
                    relationSet.add((indexDict[key]['name'], key, 'Association', at, reverseClassDict[at]['id']))
                    messages.add((at, 'Dangerous Calls', indexDict[key]['name']))
            elif at in autoInterfaceSet:
                if indexDict[key]['name'] != at:
                    relationSet.add((indexDict[key]['name'], key, 'Association', at, reverseClassDict[at]['id']))
                    messages.add((at, 'Dangerous Calls', indexDict[key]['name']))
            else:
                continue
        # 通过成员方法简单判断实体
        methods = classNodeDict[key]['methods']
        attrsName = [attr[3].lower() for attr in attrs]
        methodsName = [met[3].lower() for met in methods]
        tmp_get = set()
        tmp_set = set()
        for met in methodsName:
            preName = met[:3]
            postName = met[3:]
            if preName == 'get':
                tmp_get.add(postName)
            elif preName == 'set':
                tmp_set.add(postName)
            else:
                continue
        if tmp_get.__len__() * 2 == methodsName.__len__() and tmp_set.__len__() == attrsName.__len__() and tmp_set.__len__() == tmp_get.__len__():
            entityClass[key] = {}
            entityClass[key]['name'] = classNodeDict[key]['name']
            entityClass[key]['value'] = 0.0
    # 处理物理节点
    deploymentNodeList = deploymentViewNode.findall('.//packagedElement', ns)
    deploymentDict = {}
    systemDict = {}
    deviceDict = {}
    deploymentRelationSet = set()

    for dep in deploymentNodeList:
        if dep.get('{' + ns['xmi'] + '}type') == 'uml:Node':
            deploymentDict[dep.get('{' + ns['xmi'] + '}id')] = {'name': dep.attrib['name']}
            indexDict[dep.get('{' + ns['xmi'] + '}id')] = {'name': dep.attrib['name'], 'type': 'Node'}
        elif dep.get('{' + ns['xmi'] + '}type') == 'uml:ExecutionEnvironment':
            systemDict[dep.get('{' + ns['xmi'] + '}id')] = {'name': dep.attrib['name']}
            indexDict[dep.get('{' + ns['xmi'] + '}id')] = {'name': dep.attrib['name'], 'type': 'Node'}
        elif dep.get('{' + ns['xmi'] + '}type') == 'uml:Device':
            deviceDict[dep.get('{' + ns['xmi'] + '}id')] = {'name': dep.attrib['name']}
            indexDict[dep.get('{' + ns['xmi'] + '}id')] = {'name': dep.attrib['name'], 'type': 'Node'}
        else:
            continue
    # 部署节点
    for key in deploymentDict.keys():
        elementNode = root.find('*/elements/element[@xmi:idref="' + key + '"]', ns)
        if elementNode is None:
            raise Exception(key + "元素无法找到")
        # 找到属性节点
        propNode = elementNode.find('./properties', ns)
        if propNode is None:
            raise Exception(key + "无属性节点")
        deploymentDict[key]['visibility'] = propNode.attrib['scope']
        # 查找组件包含的类成员
        # 'attrs':[[权限, 修饰符, 类型, 变量名], ... ]
        attrNodeList = elementNode.findall("./attributes/attribute", ns)
        attrs = []
        for attr in attrNodeList:
            attrScope = attr.get('scope')
            attrPropNode = attr.find("./properties")
            attrStatic = attrPropNode.get('static')
            propList = []
            if attrStatic == "1":
                propList.append('static')
            attrFinal = attrPropNode.get('changeability')
            if attrFinal == "frozen":
                propList.append('final')
            attrType = attrPropNode.get('type')
            attrName = attr.get('name')
            attrs.append([attrScope, propList, attrType, attrName])
            deploymentRelationSet.add((deploymentDict[key]['name'], key, 'Node Contain', attrType, reverseComponentDict[attrType]['id']))
        deploymentDict[key]['attrs'] = attrs
        # 节点间关系
        linkNode = elementNode.find('./links', ns)
        if linkNode is not None:
            for relationNode in linkNode.iter():
                relation_tmp = relationNode.tag
                if relation_tmp != 'links':
                    startDeployment = indexDict[relationNode.attrib['start']]['name']
                    endDeployment = indexDict[relationNode.attrib['end']]['name']
                    deploymentRelationSet.add((startDeployment, relationNode.attrib['start'], relation_tmp, endDeployment, relationNode.attrib['end']))
                    if relation_tmp == 'Association':
                        deploymentRelationSet.add((endDeployment, relationNode.attrib['end'], relation_tmp, startDeployment, relationNode.attrib['start']))

    # 环境节点
    for key in systemDict.keys():
        elementNode = root.find('*/elements/element[@xmi:idref="' + key + '"]', ns)
        if elementNode is None:
            raise Exception(key + "元素无法找到")
        # 找到属性节点
        propNode = elementNode.find('./properties', ns)
        if propNode is None:
            raise Exception(key + "无属性节点")
        systemDict[key]['visibility'] = propNode.attrib['scope']
        # 查找组件包含的类成员
        # 'attrs':[[权限, 修饰符, 类型, 变量名], ... ]
        attrNodeList = elementNode.findall("./attributes/attribute", ns)
        attrs = []
        for attr in attrNodeList:
            attrScope = attr.get('scope')
            attrPropNode = attr.find("./properties")
            attrStatic = attrPropNode.get('static')
            propList = []
            if attrStatic == "1":
                propList.append('static')
            attrFinal = attrPropNode.get('changeability')
            if attrFinal == "frozen":
                propList.append('final')
            attrType = attrPropNode.get('type')
            attrName = attr.get('name')
            attrs.append([attrScope, propList, attrType, attrName])
            deploymentRelationSet.add((systemDict[key]['name'], key, 'Node Contain', attrType, reverseComponentDict[attrType]['id']))
        systemDict[key]['attrs'] = attrs
        # 节点间关系
        linkNode = elementNode.find('./links', ns)
        if linkNode is not None:
            for relationNode in linkNode.iter():
                relation_tmp = relationNode.tag
                if relation_tmp != 'links':
                    startDeployment = indexDict[relationNode.attrib['start']]['name']
                    endDeployment = indexDict[relationNode.attrib['end']]['name']
                    deploymentRelationSet.add((startDeployment, relationNode.attrib['start'], relation_tmp, endDeployment, relationNode.attrib['end']))
                    if relation_tmp == 'Association':
                        deploymentRelationSet.add((endDeployment, relationNode.attrib['end'], relation_tmp, startDeployment, relationNode.attrib['start']))

    # 设备节点
    for key in deviceDict.keys():
        elementNode = root.find('*/elements/element[@xmi:idref="' + key + '"]', ns)
        if elementNode is None:
            raise Exception(key + "元素无法找到")
        # 找到属性节点
        propNode = elementNode.find('./properties', ns)
        if propNode is None:
            raise Exception(key + "无属性节点")
        deviceDict[key]['visibility'] = propNode.attrib['scope']
        # 查找组件包含的类成员
        # 'attrs':[[权限, 修饰符, 类型, 变量名], ... ]
        attrNodeList = elementNode.findall("./attributes/attribute", ns)
        attrs = []
        for attr in attrNodeList:
            attrScope = attr.get('scope')
            attrPropNode = attr.find("./properties")
            attrStatic = attrPropNode.get('static')
            propList = []
            if attrStatic == "1":
                propList.append('static')
            attrFinal = attrPropNode.get('changeability')
            if attrFinal == "frozen":
                propList.append('final')
            attrType = attrPropNode.get('type')
            attrName = attr.get('name')
            attrs.append([attrScope, propList, attrType, attrName])
            deploymentRelationSet.add((deviceDict[key]['name'], key, 'Node Contain', attrType, reverseComponentDict[attrType]['id']))
        deviceDict[key]['attrs'] = attrs
        # 节点间关系
        linkNode = elementNode.find('./links', ns)
        if linkNode is not None:
            for relationNode in linkNode.iter():
                relation_tmp = relationNode.tag
                if relation_tmp != 'links':
                    startDeployment = indexDict[relationNode.attrib['start']]['name']
                    endDeployment = indexDict[relationNode.attrib['end']]['name']
                    deploymentRelationSet.add((startDeployment, relationNode.attrib['start'], relation_tmp, endDeployment, relationNode.attrib['end']))
                    if relation_tmp == 'Association':
                        deploymentRelationSet.add((endDeployment, relationNode.attrib['end'], relation_tmp, startDeployment, relationNode.attrib['start']))
    deployDict = {}
    for key in deploymentDict.keys():
        deployDict[key] = deploymentDict[key]
    for key in systemDict.keys():
        deployDict[key] = systemDict[key]
    for key in deviceDict.keys():
        deployDict[key] = deviceDict[key]

    # 时序图
    sequenceObjectNodeList = root.findall('*/elements/element[@xmi:type="uml:Object"]', ns)
    ActorNodeList = root.findall('*/elements/element[@xmi:type="uml:Actor"]', ns)
    sequencePackageDict = {}
    sequenceObjectDict = {}
    sequenceActorDict = {}
    packageSet = set()
    messageSet = set()
    messageDict = {}

    # 记录包中的内容
    for elementNode in sequenceObjectNodeList:
        modelNode = elementNode.find('./model', ns)
        if modelNode is None:
            raise Exception('没有model节点'+elementNode.get('{' + ns['xmi'] + '}idref'))
        packageId = modelNode.attrib['package']
        propNode = elementNode.find('./properties', ns)
        objectId = elementNode.get('{' + ns['xmi'] + '}idref')
        objectType = propNode.attrib['classname']
        objectEntity = propNode.get('stereotype')
        if objectEntity is None:
            objectEntity = 'False'
        else:
            objectEntity = 'True'
        if packageId not in packageSet:
            packageSet.add(packageId)
            packageNode = root.find('*/elements/element[@xmi:idref="'+packageId+'"]', ns)
            # object:[(objectNodeId, objectType, objectIsEntity)]
            sequencePackageDict[packageId] = {'name': packageNode.attrib['name'], 'actor': [], 'object': [(objectId, objectType, objectEntity)]}
        else:
            sequencePackageDict[packageId]['object'].append((objectId, objectType, objectEntity))
        # name属性的值就是该Object的类型
        sequenceObjectDict[objectId] = {'name': objectType}
        linkNode = elementNode.find('./links')
        if linkNode is not None:
            for relationNode in linkNode.iter():
                relation_tmp = relationNode.tag
                if relation_tmp != 'links':
                    messageId = relationNode.get('{' + ns['xmi'] + '}id')
                    connectNode = root.find('*/connectors/connector[@xmi:idref="' + messageId + '"]', ns)
                    if connectNode is None:
                        raise Exception('Can not find SequenceConnector!' + messageId)
                    extendedProperties = connectNode.find('./extendedProperties', ns)
                    synch = extendedProperties.attrib['privatedata1']  # Asynchronous or Synchronous
                    messageSet.add((messageId, relationNode.attrib['start'], relationNode.attrib['end']))
                    messageDict[messageId] = {'start': relationNode.attrib['start'], 'end': relationNode.attrib['end'], 'synch': synch}

    for elementNode in ActorNodeList:
        modelNode = elementNode.find('./model', ns)
        if modelNode is None:
            raise Exception('没有model节点'+elementNode.get('{' + ns['xmi'] + '}idref'))
        packageId = modelNode.attrib['package']
        propNode = elementNode.find('./properties', ns)
        objectId = elementNode.get('{' + ns['xmi'] + '}idref')
        if packageId in packageSet:
            sequenceActorDict[objectId] = {'name': elementNode.attrib['name']}
            sequencePackageDict[packageId]['actor'].append(objectId)
            linkNode = elementNode.find('./links')
            if linkNode is not None:
                for relationNode in linkNode.iter():
                    relation_tmp = relationNode.tag
                    if relation_tmp != 'links':
                        messageId = relationNode.get('{' + ns['xmi'] + '}id')
                        connectNode = root.find('*/connectors/connector[@xmi:idref="' + messageId + '"]', ns)
                        if connectNode is None:
                            raise Exception('Can not find SequenceConnector!' + messageId)
                        extendedProperties = connectNode.find('./extendedProperties', ns)
                        synch = extendedProperties.attrib['privatedata1']  # Asynchronous or Synchronous
                        messageSet.add((messageId, relationNode.attrib['start'], relationNode.attrib['end']))
                        messageDict[messageId] = {'start': relationNode.attrib['start'], 'end': relationNode.attrib['end'], 'synch': synch}
    actorKeySet = set(sequenceActorDict.keys())
    objectKeySet = set(sequenceObjectDict.keys())
    for mID, rS, rE in messageSet:
        connectNode = root.find('*/connectors/connector[@xmi:idref="' + mID + '"]', ns)
        if rS in actorKeySet:
            sender = 'Actor'
        else:
            sender = sequenceObjectDict[rS]['name']
        if rE in actorKeySet:
            receiver = 'Actor'
        else:
            receiver = sequenceObjectDict[rE]['name']
        # messages.add((sender, connectNode.attrib['name'], receiver))
        try:
            messageDict[mID]['sender'] = sender
            messageDict[mID]['receiver'] = receiver
            messages.add((sender, connectNode.attrib['name'], receiver))
        except:
            print(sender, connectNode.attrib, receiver)
    tmpSet = set()
    tmpDict = {}
    for rS, rM, rE in messages:
        tmpKey = rS + '.' + rE
        if tmpKey in tmpSet:
            tmpDict[tmpKey].append(rM)
        else:
            tmpSet.add(tmpKey)
            tmpDict[tmpKey] = [rM]

    messages.clear()
    for key in tmpDict.keys():
        rM = '|'.join(tmpDict[key])
        rst = key.split('.')
        rS = rst[0]
        rE = rst[1]
        messages.add((rS, rM, rE))

    sequenceMessageIds = {}
    # 获取时序图中message的顺序
    for key in sequencePackageDict.keys():
        tempPackageNode = sequenceViewNode.find('./packagedElement[@xmi:id="' + key + '"]', ns)
        if tempPackageNode is None:
            raise Exception('Can not find SequencePackage!' + key)
        tempMessages = {}
        idx = 0
        messageKeyList = []
        for tm in tempPackageNode.iter('message'):
            messageId = tm.get('{' + ns['xmi'] + '}id')
            connectNode = root.find('*/connectors/connector[@xmi:idref="' + messageId + '"]', ns)
            if connectNode is None:
                raise Exception('Can not find SequenceConnector!' + messageId)
            extendedProperties = connectNode.find('./extendedProperties', ns)
            synch = extendedProperties.attrib['privatedata1']  # Asynchronous or Synchronous
            messageName = tm.get('name')
            messageKeyList.append(messageDict[messageId]['receiver']+'.'+messageName)
            tempMessages[str(idx)+'.'+messageDict[messageId]['receiver']+'.'+messageName] = {'index': idx, 'name': messageName, 'id': messageId, 'sender': messageDict[messageId]['sender'], 'receiver': messageDict[messageId]['receiver'], 'synch': synch}
            idx += 1
        sequenceMessageIds[sequencePackageDict[key]['name']] = {'id': key, 'messages': tempMessages, 'nameList': messageKeyList}

    # 用例图
    useCaseNodeDict = {}
    useCaseActorDict = {}
    useCasePackageSet = set()
    useCasePackageDict = {}
    useCaseRelation = set()

    useCaseNodeList = root.findall('*/elements/element[@xmi:type="uml:UseCase"]', ns)
    for elementNode in useCaseNodeList:
        modelNode = elementNode.find('./model', ns)
        if modelNode is None:
            raise Exception('没有model节点' + elementNode.get('{' + ns['xmi'] + '}idref'))
        packageId = modelNode.attrib['package']
        useCaseId = elementNode.get('{' + ns['xmi'] + '}idref')
        useCaseName = elementNode.attrib['name']
        if packageId not in useCasePackageSet:
            useCasePackageSet.add(packageId)
            packageNode = root.find('*/elements/element[@xmi:idref="'+packageId+'"]', ns)
            # object:[(objectNodeId, objectType, objectIsEntity)]
            useCasePackageDict[packageId] = {'name': packageNode.attrib['name'], 'actor': [], 'useCase': [(useCaseId, useCaseName)]}
        else:
            useCasePackageDict[packageId]['useCase'].append((useCaseId, useCaseName))
        useCaseNodeDict[useCaseId] = {'name': useCaseName, 'type': 'Use Case'}
        linkNode = elementNode.find('./links')
        if linkNode is not None:
            for relationNode in linkNode.iter():
                relation_tmp = relationNode.tag
                if relation_tmp != 'links':
                    linkId = relationNode.get('{' + ns['xmi'] + '}id')
                    useCaseRelation.add((linkId, relation_tmp, relationNode.attrib['start'], relationNode.attrib['end']))

    for elementNode in ActorNodeList:
        modelNode = elementNode.find('./model', ns)
        if modelNode is None:
            raise Exception('没有model节点'+elementNode.get('{' + ns['xmi'] + '}idref'))
        packageId = modelNode.attrib['package']
        propNode = elementNode.find('./properties', ns)
        actorId = elementNode.get('{' + ns['xmi'] + '}idref')
        if packageId in useCasePackageSet:
            useCaseActorDict[actorId] = {'name': elementNode.attrib['name']}
            useCasePackageDict[packageId]['actor'].append(actorId)
            linkNode = elementNode.find('./links')
            if linkNode is not None:
                for relationNode in linkNode.iter():
                    relation_tmp = relationNode.tag
                    if relation_tmp != 'links':
                        linkId = relationNode.get('{' + ns['xmi'] + '}id')
                        useCaseRelation.add((linkId, relation_tmp, relationNode.attrib['start'], relationNode.attrib['end']))

    caseRelations = set()
    caseActorSet = set(useCaseActorDict.keys())
    caseSet = set(useCaseNodeDict.keys())
    for rID, rType, rS, rE in useCaseRelation:
        if rS in caseActorSet:
            sender = useCaseActorDict[rS]['name']
        else:
            sender = useCaseNodeDict[rS]['name']
        if rE in caseActorSet:
            receiver = useCaseActorDict[rE]['name']
        else:
            receiver = useCaseNodeDict[rE]['name']
        if rType == 'UseCase':
            connectNode = root.find('*/connectors/connector[@xmi:idref="' + rID + '"]', ns)
            propNode = connectNode.find('./properties', ns)
            caseRelations.add((sender, propNode.attrib['subtype'], receiver))
        else:
            caseRelations.add((sender, rType, receiver))

    actorCaseMap = {}
    for s, r, t in caseRelations:
        if s in actorCaseMap.keys():
            if r != 'Generalization' and r != 'Extends':
                actorCaseMap[s]['child'].add(t)
                if t in actorCaseMap.keys():
                    actorCaseMap[t]['parent'].add(s)
                else:
                    actorCaseMap[t] = {'child': set(), 'parent': {s}}
            else:
                if t in actorCaseMap.keys():
                    actorCaseMap[t]['child'].add(s)
                else:
                    actorCaseMap[t] = {'child': {s}, 'parent': set()}
                actorCaseMap[s]['parent'].add(t)
        else:
            if r != 'Generalization' and r != 'Extends':
                actorCaseMap[s] = {'child': {t}, 'parent': set()}
                if t in actorCaseMap.keys():
                    actorCaseMap[t]['parent'].add(s)
                else:
                    actorCaseMap[t] = {'child': set(), 'parent': {s}}
            else:
                if t in actorCaseMap.keys():
                    actorCaseMap[t]['child'].add(s)
                else:
                    actorCaseMap[t] = {'child': {s}, 'parent': set()}
                actorCaseMap[s] = {'child': set(), 'parent': {t}}

    for key in actorCaseMap.keys():
        if actorCaseMap[key]['parent'].__len__() == 0:
            continue
        else:
            for p in actorCaseMap[key]['parent']:
                actorCaseMap[p]['child'].update(actorCaseMap[key]['child'])

    keyList = list(actorCaseMap.keys())
    for key in keyList:
        if actorCaseMap[key]['parent'].__len__() == 0:
            continue
        else:
            actorCaseMap.pop(key)

    # 活动图解析
    activityViewSet = set()
    activityPackageSet = set()
    activityViewDict = {}
    activityPackageDict = {}
    actionSet = set()
    actionDict = {}
    class4case = {}
    case4class = {}

    # 直接从packagedElement读取包，节点， 边
    packageList = activeViewNode.findall('./packagedElement[@xmi:type="uml:Package"]', ns)
    for package in packageList:
        activityViewId = package.get('{' + ns['xmi'] + '}id')
        if activityViewId not in activityViewSet:
            activityViewDict[activityViewId] = {'name': package.attrib['name'], 'activities': {}, 'nodes': {},
                                                'edges': {}, 'initNode': set(), 'finalNode': set(), 'edgeSet': set()}
            activityViewSet.add(activityViewId)
        # activityViewPackage = {}
        activitiesList = package.findall('./packagedElement', ns)
        for at in activitiesList:
            activityPackageId = at.get('{' + ns['xmi'] + '}id')
            if activityPackageId not in activityPackageSet:
                activityPackageDict[activityPackageId] = {'nodes': {}, 'edges': {}}
                activityPackageSet.add(activityPackageId)
                activityViewDict[activityViewId]['activities'][activityPackageId] = {'name': at.get('name')}
            activityNodeList = at.findall('./node', ns)
            for an in activityNodeList:
                nodeId = an.get('{' + ns['xmi'] + '}id')
                nodeName = an.get('name')
                nodeType = an.get('{' + ns['xmi'] + '}type').split(':')[-1]
                operationNode = an.find('.//operation')
                if operationNode is None:
                    operationId = None
                    optParentType = None
                    optParent = None
                    opt = None
                    elementNode = root.find('*/elements/element[@xmi:idref="' + nodeId + '"]', ns)
                    if elementNode is None:
                        raise Exception(nodeId + "元素无法找到")
                    # 找到属性节点
                    propertyNode = elementNode.find('properties', ns)
                    if 'alias' in propertyNode.attrib.keys():
                        alias = propertyNode.attrib['alias']
                    elif nodeType == 'InitialNode':
                        alias = "Begin"
                    elif nodeType == 'ActivityFinalNode':
                        alias = "Final"
                else:
                    operationId = operationNode.get('{' + ns['xmi'] + '}idref')
                    # eleOptNode = classViewNode.find('*/ownedOperation[@xmi:id='+operationId+']', ns)
                    optParentType = operationMap[operationId]['parentType']
                    optParent = operationMap[operationId]['parent']
                    # 类->业务
                    if optParent in class4case.keys():
                        class4case[optParent].add(package.attrib['name'])
                    else:
                        class4case[optParent] = {package.attrib['name']}
                    # 业务->类
                    if package.attrib['name'] in case4class.keys():
                        case4class[package.attrib['name']].add(optParent)
                    else:
                        case4class[package.attrib['name']] = {optParent}
                    opt = operationMap[operationId]['operation']
                    optKey = optParent + "." + opt
                    if optKey in actionSet:
                        actionDict[optKey]['activityView'].add(activityViewId)
                    else:
                        actionDict[optKey] = {'activityView': {activityViewId}, 'frequency': 0}
                        actionSet.add(optKey)
                    alias = optKey
                activityViewDict[activityViewId]['nodes'][nodeId] = {'name': nodeName, 'type': nodeType,
                                                                     'operationId': operationId, 'optParent': optParent,
                                                                     'optParentType': optParentType, 'operation': opt, 'alias': alias}
                activityPackageDict[activityPackageId]['nodes'][nodeId] = {'name': nodeName, 'type': nodeType,
                                                                           'operationId': operationId,
                                                                           'optParent': optParent,
                                                                           'optParentType': optParentType,
                                                                           'operation': opt, 'alias': alias}
                if nodeType == 'InitialNode':
                    activityViewDict[activityViewId]['initNode'].add(nodeId)
                elif nodeType == 'ActivityFinalNode':
                    activityViewDict[activityViewId]['finalNode'].add(nodeId)
            activityEdgeList = at.findall('./edge', ns)
            for ae in activityEdgeList:
                edgeId = ae.get('{' + ns['xmi'] + '}id')
                edgeName = ae.get('name')
                edgeType = ae.get('{' + ns['xmi'] + '}type').split(':')[-1]
                edgeSource = ae.get('source')
                edgeTarget = ae.get('target')
                activityViewDict[activityViewId]['edges'][edgeId] = {'name': edgeName, 'type': edgeType,
                                                                     'source': edgeSource, 'target': edgeTarget}
                activityPackageDict[activityPackageId]['edges'][edgeId] = {'name': edgeName, 'type': edgeType,
                                                                           'source': edgeSource, 'target': edgeTarget}
        edgesDict = activityViewDict[activityViewId]['edges']
        for edgeKey in edgesDict.keys():
            edgeSource = edgesDict[edgeKey]['source']
            edgeTarget = edgesDict[edgeKey]['target']
            if activityViewDict[activityViewId]['nodes'][edgeSource]['optParent'] is not None:
                if activityViewDict[activityViewId]['nodes'][edgeTarget]['optParent'] is not None:
                    activityViewDict[activityViewId]['edgeSet'].add(((activityViewDict[activityViewId]['nodes'][
                        edgeSource]['optParent'], True), (
                        activityViewDict[activityViewId]['nodes'][
                            edgeTarget]['optParent'], True)))
                elif activityViewDict[activityViewId]['nodes'][edgeTarget]['type'] == 'ActivityFinalNode':
                    activityViewDict[activityViewId]['edgeSet'].add(((activityViewDict[activityViewId]['nodes'][
                        edgeSource]['optParent'], True),
                        ('FinalNode', False)))
                elif activityViewDict[activityViewId]['nodes'][edgeTarget]['type'] == 'InitialNode':
                    activityViewDict[activityViewId]['edgeSet'].add(((activityViewDict[activityViewId]['nodes'][
                        edgeSource]['optParent'], True),
                        ('BeginNode', False)))
                else:
                    activityViewDict[activityViewId]['edgeSet'].add(((activityViewDict[activityViewId]['nodes'][
                        edgeSource]['optParent'], True),
                        (edgeTarget, False)))
            elif activityViewDict[activityViewId]['nodes'][edgeSource]['type'] == 'InitialNode':
                if activityViewDict[activityViewId]['nodes'][edgeTarget]['optParent'] is not None:
                    activityViewDict[activityViewId]['edgeSet'].add((('BeginNode', False), (
                        activityViewDict[activityViewId]['nodes'][edgeTarget]['optParent'], True)))
                elif activityViewDict[activityViewId]['nodes'][edgeTarget]['type'] == 'ActivityFinalNode':
                    activityViewDict[activityViewId]['edgeSet'].add((('BeginNode', False), ('FinalNode', False)))
                elif activityViewDict[activityViewId]['nodes'][edgeTarget]['type'] == 'InitialNode':
                    activityViewDict[activityViewId]['edgeSet'].add((('BeginNode', False), ('BeginNode', False)))
                else:
                    activityViewDict[activityViewId]['edgeSet'].add((('BeginNode', False), (edgeTarget, False)))
            elif activityViewDict[activityViewId]['nodes'][edgeSource]['type'] == 'ActivityFinalNode':
                if activityViewDict[activityViewId]['nodes'][edgeTarget]['optParent'] is not None:
                    activityViewDict[activityViewId]['edgeSet'].add((('FinalNode', False), (
                        activityViewDict[activityViewId]['nodes'][edgeTarget]['optParent'], True)))
                elif activityViewDict[activityViewId]['nodes'][edgeTarget]['type'] == 'ActivityFinalNode':
                    activityViewDict[activityViewId]['edgeSet'].add((('FinalNode', False), ('FinalNode', False)))
                elif activityViewDict[activityViewId]['nodes'][edgeTarget]['type'] == 'InitialNode':
                    activityViewDict[activityViewId]['edgeSet'].add((('FinalNode', False), ('BeginNode', False)))
                else:
                    activityViewDict[activityViewId]['edgeSet'].add((('FinalNode', False), (edgeTarget, False)))
            else:
                if activityViewDict[activityViewId]['nodes'][edgeTarget]['optParent'] is not None:
                    activityViewDict[activityViewId]['edgeSet'].add(((edgeSource, False), (
                        activityViewDict[activityViewId]['nodes'][edgeTarget]['optParent'], True)))
                elif activityViewDict[activityViewId]['nodes'][edgeTarget]['type'] == 'ActivityFinalNode':
                    activityViewDict[activityViewId]['edgeSet'].add(((edgeSource, False), ('FinalNode', False)))
                elif activityViewDict[activityViewId]['nodes'][edgeTarget]['type'] == 'InitialNode':
                    activityViewDict[activityViewId]['edgeSet'].add(((edgeSource, False), ('BeginNode', False)))
                else:
                    activityViewDict[activityViewId]['edgeSet'].add(((edgeSource, False), (edgeTarget, False)))

    # 修正Fork和Join节点
    # 将活动图转换为边的表示用于生成活动图路径
    activeEdgesDict = {}
    for viewKey in activityViewDict.keys():
        edges = activityViewDict[viewKey]['edges']
        targetSet = {}
        activeEdgesDict[viewKey] = {"name": activityViewDict[viewKey]['name'], "edges": []}
        for edgeKey in edges.keys():
            source = edges[edgeKey]['source']
            target = edges[edgeKey]['target']
            sourceNode = activityViewDict[viewKey]['nodes'][source]
            targetNode = activityViewDict[viewKey]['nodes'][target]
            if source not in targetSet:
                targetSet[source] = {'out': 1, 'in': 0}
            else:
                targetSet[source]['out'] += 1
            if target not in targetSet:
                targetSet[target] = {'out': 0, 'in': 1}
            else:
                targetSet[target]['in'] += 1
            if (sourceNode['alias'], targetNode['alias']) not in activeEdgesDict[viewKey]['edges']:
                activeEdgesDict[viewKey]['edges'].append((sourceNode['alias'], targetNode['alias']))
        for nodeKey in activityViewDict[viewKey]['nodes'].keys():
            if activityViewDict[viewKey]['nodes'][nodeKey]['type'] == 'ForkNode':
                if targetSet[nodeKey]['in'] > 1:
                    activityViewDict[viewKey]['nodes'][nodeKey]['type'] = 'JoinNode'

    business_paths = {}
    # 生成活动图路径
    for key in activeEdgesDict.keys():
        edges = activeEdgesDict[key]['edges']
        business_paths[activeEdgesDict[key]['name']] = {}
        node_set = set()
        for s, t in edges:
            node_set.add(s)
            node_set.add(t)
        new_paths = run(edges)
        for pdx, path in enumerate(new_paths):
            new_nodes = set()
            remove_list = []
            idx = 0
            dm_edges_idx = []
            fj_edges_idx = []
            while "Decision" + str(idx+1) in path:
                idx += 1
                dm_edges_idx.append(idx)
            idx = 0
            while "Fork" + str(idx+1) in path:
                idx += 1
                fj_edges_idx.append(idx)
            for node in path:
                new_nodes.add(node)
            for node in node_set:
                if node not in new_nodes:
                    remove_list.append(node)
            G = nx.DiGraph()
            G.add_edges_from(edges)
            for node in remove_list:
                G.remove_node(node)
            for idx in dm_edges_idx:
                if G.has_edge("Decision" + str(idx), "Merge" + str(idx)):
                    G.remove_edge("Decision" + str(idx), "Merge" + str(idx))
            for idx in fj_edges_idx:
                if G.has_edge("Fork" + str(idx), "Join" + str(idx)):
                    G.remove_edge("Fork" + str(idx), "Join" + str(idx))
            business_paths[activeEdgesDict[key]['name']]['path'+str(pdx)] = {}
            business_paths[activeEdgesDict[key]['name']]['path'+str(pdx)]["plist"] = path
            business_paths[activeEdgesDict[key]['name']]['path'+str(pdx)]["elist"] = list(G.edges())
            # G.clear()
    return classNodeDict, componentDict, actorCaseMap, deployDict, sequenceMessageIds, business_paths


def business_respo(classNodeDict, componentDict, actorCaseMap, deployDict, sequenceMessageIds, business_paths):
    c_opt = {}
    for key in classNodeDict.keys():
        c = classNodeDict[key]['name']
        opt_list = classNodeDict[key]['methods']
        c_opt[c] = []
        for opt in opt_list:
            opt_name = opt[3]
            parms = opt[4]
            # 准备拼接类.方法
            parms_list = [i for (i, j) in parms]
            parms_str = ", ".join(parms_list)
            opt_str = c + "." + opt_name + "(" + parms_str + ")"
            c_opt[c].append(opt_str)
    comp_c = {}
    for key in componentDict.keys():
        comp = componentDict[key]['name']
        c_list = componentDict[key]['attrs']
        comp_c[comp] = []
        for c in c_list:
            c_name = opt[2]
            comp_c[comp].append(c_name)
    dep_comp = {}
    for key in deployDict.keys():
        deploy = deployDict[key]['name']
        comp_list = deployDict[key]['attrs']
        dep_comp[deploy] = []
        for comp in comp_list:
            comp_name = comp[2]
            dep_comp[deploy].append(comp_name)
    reversed_dict = {}
    for dep in dep_comp.keys():
        for comp in dep_comp[dep]:
            for c in comp_c[comp]:
                if c in reversed_dict.keys():
                    reversed_dict[c].append(dep+'.'+comp+'.'+c)
                else:
                    reversed_dict[c] = [dep+'.'+comp+'.'+c]


if __name__ == '__main__':
    import os
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../')
    classNodeDict, componentDict, actorCaseMap, deployDict, sequenceMessageIds, business_paths = xmlAnalyse(path+'/architecture/LMS-async-ForkJoin.xml')
    # print(classNodeDict)
    # print("---------------")
    # print(componentDict)
    # print("----------------")
    # print(actorCaseMap)
    # print("---------------")
    # print(deployDict)
    # print("----------------")
    # print(sequenceMessageIds)
    # print("---------------")
    for key in business_paths.keys():
        print(key)
        print(business_paths[key])
