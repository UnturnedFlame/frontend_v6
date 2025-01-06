<template>
  <a-button class="private-algorithm-button" ghost @click="uploadPrivateAlgorithmFiles()">
    <i class="fa-solid fa-cloud-arrow-up" style="margin-right: 3px;"></i>
    <span style="font-family: 'Microsoft YaHei';">上传组件</span>
  </a-button>
  <!-- 上传增值服务组件的操作面板 -->
  <a-modal
    v-model:open="dialogVisible"
    title="上传增值服务组件"
    cancelText="取消"
    :ok-button-props="{ style: { display: 'none' } }"
    :cancel-button-props="{ style: { display: 'none' } }"
  >
    <div
      style="
        display: flex;
        padding: 10px;
        flex-direction: column;
        justify-content: center;
        font-family: 'Microsoft YaHei';
      "
    >
      <div style="width: 100%">
        <!-- 选择组件的算法类型 -->
        <div style="width: 100%; margin-bottom: 10px">
          <span><span style="color: red">*</span>选择上传组件的类型：</span>
      
          <a-tree-select
            v-model:value="uploadAlgorithmForm.algorithmType"
            show-search
            style="width: 40%"
            :dropdown-style="{ maxHeight: '400px', overflow: 'auto' }"
            placeholder="请选择要上传的组件类型"
            tree-default-expand-all
            :tree-data="treeData"
            tree-node-filter-prop="label"
            @change="algorithmTypeChange"
          >
            <template #title="{ value: val, label }">
              <b v-if="val === 'parent 1-1'" style="color: #08c">sss</b>
              <template v-else>{{ label }}</template>
            </template>
          </a-tree-select>
        </div>

        <!-- 当上传无量纲化算法时，需要进一步选择是提取特征还是原始信号进行无量纲化 -->
        <div
          style="padding-top: 0; padding-bottom: 10px"
          v-if="uploadAlgorithmForm.algorithmType === '无量纲化'"
        >
          <span><span style="color: red">*</span>选择无量纲化的对象：</span>
          <a-radio-group v-model:value="uploadAlgorithmForm.useLog" name="gradioGroup">
            <a-radio :value="false">对原始信号无量纲化</a-radio>
            <a-radio :value="true">对提取的特征无量纲化</a-radio>
          </a-radio-group>
        </div>

        <!-- 上传增值组件 -->
        <div style="display: flex; flex-direction: column; margin-top: 20px">
          <div style="display: flex; flex-direction: row">
            <!-- 上传增值服务的算法源文件 -->
            <div>
              <span><span style="color: red">*</span>选择要上传的源文件：</span>
              <a-upload
                :file-list="pythonFileList"
                :before-upload="beforeUploadAlgorithmFile"
                @remove="removePythonFile"
                :maxCount="1"
              >
                <a-button class="upload-button" :disabled="canSelectPythonFile">
                  <upload-outlined></upload-outlined>
                  从本地选择
                </a-button>
              </a-upload>
            </div>

            <!-- 一抽屉的形式弹出相关算法模板参考 -->
            <span>
              <a-tooltip title="算法模板参考">
                <a-button
                  type="default"
                  style="color: blue; margin-left: 10px"
                  @click="showDrawer = true"
                  shape="circle"
                  :icon="h(QuestionOutlined)"
                />
              </a-tooltip>
            </span>
          </div>

          <div></div>

          <!-- 当上传故障诊断算法时，需要进一步选择是机器学习的还是深度学习的故障诊断 -->
          <div style="margin-top: 20px" v-if="uploadAlgorithmForm.algorithmType === '故障诊断'">
            <span><span style="color: red">*</span>选择所使用的模型类型：</span>
            <a-radio-group
              v-model:value="uploadAlgorithmForm.faultDiagnosisType"
              name="gradioGroup"
              @change="removeModelFile"
            >
              <a-radio value="machineLearning">机器学习模型</a-radio>
              <a-radio value="deepLearning">深度学习模型</a-radio>
            </a-radio-group>
          </div>

          <!-- 上传算法所需的模型文件 -->
          <div
            style="display: flex; flex-direction: row; margin-top: 20px"
            v-if="
              canUploadModelFile ||
              (uploadAlgorithmForm.algorithmType === '无量纲化' && uploadAlgorithmForm.useLog)
            "
          >
            <span><span style="color: red">*</span>选择使用的模型文件：</span>
            <a-upload
              :file-list="modelFileList"
              :before-upload="beforeUploadModelFile"
              @remove="removeModelFile"
              :maxCount="1"
              :auto-upload="false"
            >
              <a-button class="upload-button">
                <upload-outlined></upload-outlined>
                从本地选择
              </a-button>
            </a-upload>
          </div>
        </div>
        <div
          style="
            margin-right: 120px;
            margin-top: 20px;
            display: flex;
            flex-direction: column;
          "
        >
          <a-form
            :model="extraAlgorithmFileFormState"
            name="basic"
            ref="algorithmFileFormRef"
            :rules="rules"
            :label-col="{ span: 8 }"
            :wrapper-col="{ span: 16 }"
            autocomplete="off"
          >
            <a-form-item
              label="增值组件名称"
              name="algorithmName"
              :rules="[{ required: true, message: '请输入增值组件算法名称!' },
              { min: 3, max: 50, message: '长度应在3到50个字符之间!', trigger: 'blur' },
              { pattern: /^[\u4e00-\u9fa5a-zA-Z_][\u4e00-\u9fa5a-zA-Z0-9_-]*$/, message: '只能包含中英文、数字、下划线，且不能以数字开头!', trigger: 'blur' }]"
            >
              <a-input
                v-model:value="extraAlgorithmFileFormState.algorithmName"
                placeholder="请输入增值组件名称"
              />
              <p style="color: #999; font-size: 12px;">只能包含中英文、数字和下划线，长度不超过50个字符。</p>
            </a-form-item>

            <a-form-item
              label="增值组件描述"
              name="statement"
              :rules="[{ required: true, message: '请输入增值组件描述' },
              { min: 1, max: 200, message: '长度应在1到200个字符之间!', trigger: 'blur' }]"
            >
              <a-input
                v-model:value="extraAlgorithmFileFormState.statement"
                placeholder="请输入增值算法描述"
              />
              <p style="color: #999; font-size: 12px;">长度不超过300个字符。</p>
            </a-form-item>

            <!-- <a-form-item name="remember" :wrapper-col="{ offset: 8, span: 16 }">
              <a-checkbox v-model:checked="formState.remember">Remember me</a-checkbox>
            </a-form-item> -->

            <!-- <a-button type="primary" html-type="submit">Submit</a-button> -->
            <div style="width: 350px; margin-left: 10px; margin-bottom: 10px"
              >上传组件并进行完整性校验：</div
            >
            <a-space>
              <!-- <a-button type="primary" @click="extraModuleValidate">完整性校验</a-button> -->
              <!-- 选择一个测试样本进行组件的校验 -->
              <!-- <div style="width: 160px">
                <a-select
                  v-model:value="validateExtraAlgorithmUsingFileName"
                  style="width: 100%"
                >
                  <a-select-option
                    v-for="item in fetchedDataFiles"
                    :key="item.dataset_name"
                    :value="item.dataset_name"
                  >
                    {{ item.dataset_name }}
                  </a-select-option>
                </a-select>
              </div> -->
              <!-- <a-radio-group v-model:value="uploadAlgorithmForm.validationDataType">
                <a-radio value="single">单传感器</a-radio>
                <a-radio value="multiple">多传感器</a-radio>
              </a-radio-group> -->
              <a-button
                type="primary"
                :disabled="
                  (canUploadModelFile &&
                    (modelFileList?.length === 0 || pythonFileList?.length === 0)) ||
                  (!canUploadModelFile && pythonFileList?.length === 0)
                "
                :loading="uploading"
                @click="extraModuleUploadAndValidate"
                class="upload-button"
                style="margin-left: 10px"
              >
                {{ uploading ? "正在进行完整性校验" : "上传增值组件" }}
              </a-button>

              <!-- 显示校验结果 -->
              <span style="font-size: 20px" v-if="canShowValidationResult">
                <!-- <a-icon v-if="extraModuleValidationResult === 'success'" type="check-circle" theme="twoTone" twoToneColor="#52c41a" /> -->
                <span v-if="extraModuleValidationResult === true && !uploading" style="display: flex;align-items: center">
                  <CheckCircleOutlined style="color: green" />
                  <span style="font-size: 12px; margin-left: 5px">校验通过，上传成功</span>
                </span>

                <span v-if="extraModuleValidationResult === false && !uploading" style="display: flex;align-items: center">
                  <CloseCircleOutlined style="color: red" />
                  <span style="font-size: 12px; margin-left: 5px">校验失败</span>
                </span>
                <!-- <a-icon v-else type="close-circle" theme="twoTone" twoToneColor="#ff4d4f" /> -->
              </span>
            </a-space>
          </a-form>
        </div>
      </div>

      <!-- 显示组件的校验结果。 -->
      <div v-if="canShowValidationResult && extraModuleValidationResult" 
      style="display: flex; flex-direction: column; align-content: left; padding-top: 20px; width: 100%">
        <!-- <div v-if="extraModuleValidationResult === true">校验通过，上传成功</div> -->
        <!-- <div v-else>校验失败</div> -->
        <div style="display: flex; flex-direction: row; width: 100%">
          <span style="">所上传的组件运行结果（点击放大）</span>
          <span><a-button type="word" style="margin-left: 150px" @click="closeValidationResult">关闭</a-button></span></div>
       
        <!-- 插值处理组件校验的结果 -->
        <div v-if="canDisplayInterpolationValidationResult" style="width: 100%; height: 250px;" >
          <el-image
            :src="interpolationFigures[0]"
            :zoom-rate="1.2"
            :max-scale="7"
            :min-scale="0.2"
            :preview-src-list="interpolationFigures"
            :initial-index="4"
            fit="cover"
          />
        </div>
        <!-- 无量纲化组件校验的结果 -->
        <div v-if="canDisplayDimensionlessValidationResult" style="width: 100%; height: 250px;" >
          <el-image
            :src="dimensionlessFigures[0]"
            :zoom-rate="1.2"
            :max-scale="7"
            :min-scale="0.2"
            :preview-src-list="dimensionlessFigures"
            :initial-index="4"
            fit="cover"
          />
        </div>

        <!-- 小波变换组件校验的结果 -->
        <div v-if="canDisplayWaveletTransformValidationResult" style="width: 100%; height: 250px;" >
          <el-image
            :src="waveletTransformFigures[0]"
            :zoom-rate="1.2"
            :max-scale="7"
            :min-scale="0.2"
            :preview-src-list="waveletTransformFigures"
            :initial-index="4"
            fit="cover"
          />
        </div>

        <!-- 故障诊断组件校验的结果 -->
        <div v-if="canDisplayFaultDiagnosisValidationResult" style="width: 100%; height: auto;" >
          <el-image
            style="width: auto; height: 100px;"
            :src="faultDiagnosisFigures[0]"
            :zoom-rate="1.2"
            :max-scale="7"
            :min-scale="0.2"
            :preview-src-list="faultDiagnosisFigures"
            :initial-index="4"
            fit="cover"
          />
        </div>

        <!-- 健康评估组件校验结果 -->
        <div v-if="canDisplayHealthEvaluationValidationResult" style="width: 100%; height: auto;" >
          <el-image
            style="width: auto; height: 100px;"
            :src="healthEvaluationFigures[0]"
            :zoom-rate="1.2"
            :max-scale="7"
            :min-scale="0.2"
            :preview-src-list="healthEvaluationFigures"
          />
        </div>
        
        <!-- <div v-if="extraModuleValidationResult !== true">{{ extraModuleValidationResult }}</div> -->
      </div>

      <!-- 点击相应按钮时，显示私有算法模版参考 -->
      <!-- <a-button @click="showDrawer = true">显示算法模板参考</a-button> -->
      <a-drawer :visible="showDrawer" @close="onClose" placement="right" :closable="true">
        <span>
          <p style="font-size: 15px; font-weight: bold">上传算法模板参考</p>
          <div>
            <a-button
              v-for="algorithm in privateAlgorithms"
              @click="setAlgorithmTemplate(algorithm)"
              type="default"
            >
              {{ algorithm }}
            </a-button>
          </div>
        </span>
      </a-drawer>
      <!-- <span>
        <p style="font-size: 15px; font-weight: bold">上传算法模板参考</p>
        <div>
          <a-button
            v-for="algorithm in privateAlgorithms"
            @click="setAlgorithmTemplate(algorithm)"
            type="default"
            >{{ algorithm }}
          </a-button>
        </div>
      </span> -->
    </div>
  </a-modal>

  <!-- 私有算法参考模版 -->
  <a-modal
    v-model:open="templateDialog"
    :width="700"
    :title="templateName + '参考模版'"
    :ok-button-props="{ style: { display: 'none' } }"
    :cancel-button-props="{ style: { display: 'none' } }"
    style="font-size: 20px; font-family: 'Microsoft YaHei'"
  >
    <el-scrollbar :height="600">
      <div v-if="templateName === '插值处理'">
        <div>
          <h1>基本结构</h1>
          <h2>1. 数据输入</h2>
          <h3>插值处理的私有算法作为脚本运行时，需要从主程序获取两个参数：</h3>
          <h3>(1) --raw-data-filepath， 需要插值的原数据的存放路径</h3>
          <h3>(2) --interpolated-data-filepath， 插值后的结果数据的存放路径</h3>
          <h3>数据输入方法：通过python中的argparse库进行命令行参数的添加和解析</h3>
          <a-image :width="500" src="src/assets/interpolation-params.png" />
          <h3>
            上图为获取输入数据的示例。在获取到原数据的存放路径后，通过numpy中的load()读取原数据，即可使用相应的插值算法对其进行插值处理。
          </h3>
          <h2>2. 数据输出</h2>
          <h3>
            在完成插值处理后，使用numpy库，将对于原数据的插值结果保存到'interpolated_data_filepath'指出的存放路径
          </h3>
          <a-image :width="500" src="src/assets/interpolation-output.png"></a-image>
          <h2>3. 私有算法代码模板示例</h2>
          <h3>插值处理的私有算法模板代码如下：</h3>
          <a-image :width="500" src="src/assets/interpolation-outline.png"></a-image>
          <h3>其中'linear_interpolatin_for_signal'为用户自定义的私有插值算法</h3>
        </div>
      </div>
      <div v-if="templateName === '故障诊断'">
        <div>
          <h3>附：示例代码源文件下载链接（点击下载）</h3>
          <a
            href="src/assets/exampleCode/My-FD-Algorithm-1.py"
            download="example-fault-diagnosis.py"
            >深度学习故障诊断示例代码源文件</a
          >
          <h1>基本结构</h1>
          <h2>1. 数据输入</h2>
          <h3>故障诊断的私有算法作为脚本运行时，需要从主程序获取两个参数：</h3>
          <h3>(1) --model-filepath， 故障诊断算法所使用模型的模型参数的存放路径</h3>
          <h3>(2) --input-filepath， 样本数据的存放路径</h3>
          <h3>数据输入方法：通过python中的argparse库进行命令行参数的添加和解析</h3>
          <a-image :width="500" src="src/assets/fault-diagnosis-model-params.png" />
          <!-- <h3>在获取到原数据的存放路径后，通过numpy中的load()读取原数据，即可使用相应的插值算法对其进行插值处理。</h3> -->
          <h2>2. 模型加载</h2>
          <h3>机器学习和深度学习的模型加载方式不同</h3>
          <h3>
            (1)对于深度学习模型，在获得模型参数的存放路径之后，通过该路径加载模型参数以初始化模型，以pytorch框架为例，通过如下方式加载模型参数
          </h3>
          <a-image :width="500" src="src/assets/fault-diagnosis-load-model.png" />
          <h3>
            (2)对于机器学习模型，在获得模型的存放路径之后，通过joblib库的'load()'方法加载已训练好的模型
          </h3>
          <a-image :width="500" src="src/assets/fault-diagnosis-load-model-2.png" />
          <h3>其中注意，如果需要使用gpu辅助计算，则需要指定gpu为gpu:0</h3>
          <p style="font-size: 15px; font-weight: 600">
            以pytorch为例，通过如下代码指定使用第0块gpu：<br />
            device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
          </p>
          <!-- <code>
            device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
          </code> -->
          <h2>3. 模型推理及输出结果</h2>
          <h3>
            初始化模型之后，即可使用样本数据进行模型推理，进行模型推理之后，1代表有故障，0代表无故障，
          </h3>
          <h3>在此应该注意，注意深度学习和机器学习的故障诊断输入样本数据不同：</h3>
          <h3>
            (1)对于深度学习，其输入样本为原始的振动信号，因此使用numpy库的'numpy.load()'函数读取输入数据
          </h3>
          <h3>
            (2)对于机器学习，其输入样本为提取的手工特征，主程序中保存为pickle对象，因此使用pickle库的'pickle.load()'函数读取输入数据
          </h3>
          <h3>
            以使用pytorch框架训练的深度学习故障诊断模型为例，给出故障诊断示例代码如下
          </h3>
          <a-image :width="500" src="src/assets/fault-diagnosis-prediction.png"></a-image>
          <h3>在得到诊断结果之后，需要以打印的形式作为输出结果传回主程序</h3>
          <br />
          <h3>
            除此之外，对于机器学习的故障诊断，需要选定模型训练时的手工特征从输入数据中提取模型推理所需的特征样本，下图为机器学习的故障诊断推理示例
          </h3>
          <a-image
            :width="500"
            src="src/assets/fault-diagnosis-prediction-ml.png"
          ></a-image>
          <h3>代码中的choose_features即为该模型所需的手工特征</h3>
          <h2>4. 私有算法代码模板示例</h2>
          <h3>故障诊断的私有算法模板代码(模型结构的定义在该代码段之前)如下：</h3>
          <a-image :width="500" src="src/assets/fault-diagnosis-outline.png"></a-image>
          <h3>其中故障诊断的模型结构需要在该python源文件之中定义</h3>
          <br />
        </div>
      </div>
      <div v-if="templateName === '故障预测'">
        <div>
          <h1>基本结构</h1>
          <h2>1. 数据输入</h2>
          <h3>故障预测的私有算法作为脚本运行时，需要从主程序获取两个参数：</h3>
          <h3>(1) --model-filepath， 故障预测算法所使用模型的模型参数的存放路径</h3>
          <h3>(2) --input-filepath， 样本数据的存放路径</h3>
          <h3>数据输入方法：通过python中的argparse库进行命令行参数的添加和解析</h3>
          <a-image :width="500" src="src/assets/fault-diagnosis-model-params.png" />
          <!-- <h3>在获取到原数据的存放路径后，通过numpy中的load()读取原数据，即可使用相应的插值算法对其进行插值处理。</h3> -->
          <h2>2. 模型加载</h2>
          <h3>机器学习和深度学习的模型加载方式不同</h3>
          <h3>
            (1)如果是深度学习，在获得模型参数的存放路径之后，通过该路径加载模型参数以初始化模型，以pytorch框架为例，通过如下方式加载模型参数
          </h3>
          <a-image :width="500" src="src/assets/fault-diagnosis-load-model.png" />
          <h3>
            (2)如果是机器学习，在获得模型的存放路径之后，通过joblib库的'load()'方法加载已训练好的模型
          </h3>
          <a-image :width="500" src="src/assets/fault-diagnosis-load-model-2.png" />
          <h3>其中注意，如果需要使用gpu辅助计算，则需要指定gpu为gpu:0</h3>
          <h3></h3>
          <p style="font-size: 15px; font-weight: 600">
            以pytorch为例，通过如下代码指定使用第0块gpu：<br />
            device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
          </p>
          <!-- <code>
            device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
          </code> -->
          <h2>3. 模型推理及输出结果</h2>
          <h3>
            初始化模型之后，即可使用样本数据进行模型推理。这里注意深度学习和机器学习的样本数据不同
          </h3>
          <h3>
            (1)对于深度学习，其输入样本为原始的振动信号，因此使用numpy库的'numpy.load()'函数读取输入数据
          </h3>
          <h3>
            (2)对于机器学习，其输入样本为提取的手工特征，因此使用pickle库的'pickle.load()'函数读取输入数据
          </h3>
          <a-image :width="500" src="src/assets/fault-diagnosis-prediction.png"></a-image>
          <h3>
            其中，进行模型推理之后，得到预测的可能出现故障的时间，需要使用print()打印推理结果，以作为输出结果传回主程序，
          </h3>
          <h3>
            此时，需要注意的是在打印预测结果时，应该按照如下所示在预测结果之后紧跟'#'符号，以便于主程序读取输出的结果
          </h3>
          <a-image :width="500" src="src/assets/fault-prediction-output.png"></a-image>
          <h2>4. 私有算法代码模板示例</h2>
          <h3>故障预测的私有算法模板代码如下：</h3>
          <a-image :width="500" src="src/assets/fault-prediction-outline.png"></a-image>
        </div>
      </div>
      <!-- 无量纲化的专有算法模版 -->
      <div v-if="templateName === '无量纲化'">
        <div>
          <h1>基本结构</h1>
          <h2>1. 数据输入</h2>
          <h3>故障预测的私有算法作为脚本运行时，需要从主程序获取三个参数：</h3>
          <h3>(1) --model-filepath， 故障预测算法所使用模型的模型参数的存放路径</h3>
          <h3>(2) --input-filepath， 样本数据的存放路径</h3>
          <h3>(3) --output-filepath,，处理结果的存放路径</h3>
          <h3>数据输入方法：通过python中的argparse库进行命令行参数的添加和解析</h3>
          <a-image :width="500" src="src/assets/normalization-params.png" />
          <h3>
            其中，如果需要使用到保存的训练数据的参数对样本数据进行无量纲化处理，则应通过读取'model-filepath'路径指向的pickle文件获取训练数据参数的记录
          </h3>
          <!-- <h3>在获取到原数据的存放路径后，通过numpy中的load()读取原数据，即可使用相应的插值算法对其进行插值处理。</h3> -->
          <h3>此外，在加载数据的时候，也需要根据处理的数据的类型分类讨论：</h3>
          <a-image :width="500" src="src/assets/normalization-input.png"></a-image>
          <h3>
            如上代码示例中，如果处理的数据为提取的信号特征样本，则应该将输入样本作为.pkl类型的文件进行读取，读取到的数据类型为pandas中的DataFrame；
          </h3>
          <h3>
            而如果处理的数据为信号序列，则应该将输入样本作为.npy类型的文件进行读取，读取到的数据类型为numpy数组
          </h3>
          <h2>2. 无量纲处理以及输出结果</h2>
          <h3>在进行无量纲处理时，根据处理的数据的类型不同，处理方式也不同：</h3>
          <a-image :width="550" src="src/assets/normalization-process-output.png" />
          <h3>
            (1)如果是对于提取的特征样本，则应该在步骤1中读取保存了训练数据的记录之后，再根据该记录的训练数据的参数对输入的样本进行无量纲化，以scikit-learn中的无量纲化方法为例，
            通过已加载的参数记录对象的'transform'方法对特征样本进行标准化。同时，应该注意要提前选定训练数据使用到的特征，如上所示代码中的'choose_features'。
          </h3>
          <h3>
            (2)如果是对于信号序列，以scikit-learn中的''无量纲化方法为例，将输入数据转换为合适的形状后即可对其进行无量纲化处理。需要注意的是，主程序输入的信号序列为(1,
            2048)的numpy数组
          </h3>
          <h2>3. 专有算法代码模板示例</h2>
          <h3>无量纲化的专有算法模板代码如下：</h3>
          <a-image :width="500" src="src/assets/normalization-outline-1.png"></a-image>
          <a-image :width="500" src="src/assets/normalization-outline-2.png"></a-image>
        </div>
      </div>
      <!-- 健康评估的专有算法模板 -->
      <div v-if="templateName === '健康评估'">
        <div>
          <h3>附：示例代码源文件下载链接（点击下载）</h3>
          <a
            href="src/assets/exampleCode/My-HE-Algorithm-1.py"
            download="example-health-evaluation.py"
            >健康评估示例代码源文件</a
          >
          <h1>基本结构</h1>
          <h2>1. 数据输入</h2>
          <h3>健康评估的专有算法作为脚本运行时，需要从主程序获取参数：</h3>
          <a-image :width="550" src="src/assets/health-evaluation-params-1.png"></a-image>
          <h3>其中较为重要的参数为：</h3>
          <h3>(1) --model-filepath， 健康评估算法所使用评估模型的模型参数的存放路径</h3>
          <h3>(2) --input-filepath， 样本数据的存放路径</h3>
          <h3>(3) --save-filepath，处理结果的存放路径</h3>
          <h3>
            其余参数为层级评估模型所使用的各个参数，目前不建议修改，推荐使用默认参数。
          </h3>
          <h3>数据输入方法：通过python中的argparse库进行命令行参数的添加和解析</h3>
          <a-image :width="500" src="src/assets/health-evaluation-params-2.png" />

          <h2>2. 模型加载及模型推理</h2>

          <h3>
            层级评估模型的参数应该保存为.pkl的形式，并以.pkl文件的形式加载评估模型参数
          </h3>
          <a-image :width="500" src="src/assets/health-evaluation-load-model.png" />

          <h3>
            通过加载的评估模型，计算出权重矩阵，之后计算出层级权重指标，将计算得出的层级权重指标保存为.npy文件。
          </h3>
          <a-image :width="500" src="src/assets/health-evaluation-prediction.png" />
          <h2>3. 输出结果</h2>
          <h3>
            通过上述的模型推理得到层级权重指标矩阵之后，需要根据状态隶属度绘制出健康评估的可视化结果并给出相关建议。这里注意需要绘制层级指标权重柱状图，
          </h3>
          <h3>层级指标的树状图，并保存到'save_filepath'指出的路径下</h3>
          <a-image :width="500" src="src/assets/health-evaluation-output.png" />
          <!-- <code>
            device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
          </code> -->

          <h2>4. 私有算法代码模板示例</h2>

          <a-image :width="500" src="src/assets/health-evaluation-outline-1.png" />
          <a-image :width="500" src="src/assets/health-evaluation-outline-2.png" />
          <a-image :width="500" src="src/assets/health-evaluation-outline-3.png" />
        </div>
      </div>
      <!-- 小波变换的专有算法模板 -->
      <div v-if="templateName === '小波变换'">
        <div>
          <h1>基本结构</h1>
          <h2>1. 数据输入</h2>
          <h3>小波变换的专有算法作为脚本运行时，主要需要从主程序获取两个参数：</h3>
          <h3>(1) --input-filepath， 输入的样本数据的存放路径</h3>
          <h3>(2) --output-filepath， 处理结果数据的存放路径</h3>

          <h3>数据输入方法：通过python中的argparse库进行命令行参数的添加和解析</h3>
          <a-image :width="500" src="src/assets/wavelet-transform-params.png" />

          <h2>2. 数据处理及结果返回</h2>
          <h3>
            在通过'input-filepath'读取输入数据后，就可以根据定义的数据处理方法处理输入数据。
            然后将处理结果保存为.npy的文件以返回给主程序
          </h3>
          <a-image :width="500" src="src/assets/wavelet-transform-output.png" />

          <!-- <code>
            device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
          </code> -->

          <h2>3. 私有算法代码模板示例</h2>
          <h3>小波变换的专有算法模板代码如下：</h3>
          <a
            href="src/assets/exampleCode/My-Wavelet-1.py"
            download="example-wavelet-transform.py"
            >点击下载示例代码源文件</a
          >
          <a-image :width="500" src="src/assets/wavelet-transform-outline.png"></a-image>
          <h3>其中需要注意，定义的小波变换处理方法要在同一个源文件中。</h3>
        </div>
      </div>
    </el-scrollbar>
  </a-modal>
</template>

<script setup lang="ts">
import {
  UploadOutlined,
  QuestionOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
} from "@ant-design/icons-vue";
import { message } from "ant-design-vue";
import type { UploadProps } from "ant-design-vue";
import type { Rule } from "ant-design-vue/es/form";
import { ref, h, reactive } from "vue";
import { ElMessageBox } from "element-plus";
import { useRouter } from "vue-router";
import api from "../utils/api.js";

interface algorithmFormState {
  algorithmName: string;
  statement: string;
}
// 增值服务组件的组件名以及组件的描述
const extraAlgorithmFileFormState = reactive<algorithmFormState>({
  algorithmName: "",
  statement: "",
});

const algorithmFileFormRef = ref();

// 表单校验
const rules: Record<string, Rule[]> = {
  algorithmName: [{ required: true, message: "请输入算法名称", trigger: "blur" }],
  statement: [{ required: true, message: "请输入算法描述", trigger: "blur" }],
};

const canSelectPythonFile = ref(true);

// 私有算法
const privateAlgorithms = [
  "插值处理",
  // "特征提取",
  // "特征选择",
  "小波变换",
  "无量纲化",
  "故障诊断",
  "故障预测",
  "健康评估",
];
const templateName = ref("");

// 查看私有算法模板
const templateDialog = ref(false);

const setAlgorithmTemplate = (algorithm: string) => {
  templateName.value = algorithm;
  templateDialog.value = true;
};

const router = useRouter();
const pythonFileList = ref<UploadProps["fileList"]>([]); //算法源文件列表
const modelFileList = ref<UploadProps["fileList"]>([]); //模型源文件列表
const uploading = ref<boolean>(false);
const uploadAlgorithmForm = reactive({
  algorithmType: '', // 私有算法类型
  fileList: [],
  faultDiagnosisType: "machineLearning", // 故障诊断算法类型，可选值为machineLearning和deepLearning
  validationDataType: "single",  // 验证数据类型，可选择为单传感器和多传感器
  useLog: false, // 是否使用训练模型时的标准化方法，为true时，使用训练模型时的标准化方法，为false时，使用当前数据集的标准化方法
});

const fetchedDataFiles = ref([]);
// 从数据库获取用户已上传的数据文件
const fetchDataFiles = () => {
  let url = "user/fetch_datafiles/?publicOnly=Y";
  api.get(url).then((response: any) => {
    let datasetInfo = response.data;
    // modelsDrawer.value = false;

    fetchedDataFiles.value = [];

    for (let item of datasetInfo) {
      fetchedDataFiles.value.push(item);
    }
  });
};

const dialogVisible = ref(false);
const uploadPrivateAlgorithmFiles = () => {
  dialogVisible.value = true;
  fetchDataFiles();
};

const emit = defineEmits(["addExtraModule"]);

// 校验组件时向父组件传递的模型运行信息
let contentJson = {
  modules: [],
  algorithms: {},
  parameters: {},
  schedule: [],
  multipleSensor: false, // 是否为多传感器数据
};

// 校验插值处理增值组件
let contentJsonForInterpolation = {
  modules: ["插值处理"],
  algorithms: { 插值处理: "private_interpolation" },
  parameters: { private_interpolation: "" },
  schedule: ["数据源", "插值处理"],
  multipleSensor: false, // 是否为多传感器数据
};

// 校验小波变换增值组件
let contentJsonForWaveletTrans = {
  modules: ["小波变换"],
  algorithms: { 小波变换: "extra_wavelet_transform" },
  parameters: { extra_wavelet_transform: "" },
  schedule: ["数据源", "小波变换"],
  multipleSensor: false, // 是否为多传感器数据
};

// 校验无量纲化增值组件
let contentJsonForDimensionless = {
  modules: ["无量纲化"],
  algorithms: { 无量纲化: "private_scaler" },
  parameters: { private_scaler: { useLog: false, algorithm: "" } },
  schedule: ["数据源", "无量纲化"],
  multipleSensor: false, // 是否为多传感器数据
};

// 校验深度学习故障诊断增值组件
let contentJsonForFaultDiagnosisDL = {
  modules: ["故障诊断"],
  algorithms: { 故障诊断: "private_fault_diagnosis_deeplearning" },
  parameters: {
    private_fault_diagnosis_deeplearning: '',
  },
  schedule: ["数据源", "故障诊断"],
  mutipleSensor: false,
};

// 校验基于机器学习的故障诊断增值服务组件
let contentJsonForFaultDiagnosisML = {
  modules: ["故障诊断", "特征提取", "特征选择"],
  algorithms: {
    特征提取: "time_frequency_domain_features",
    特征选择: "correlation_coefficient_importance",
    故障诊断: "private_fault_diagnosis_machine_learning",
  },
  parameters: {
    time_frequency_domain_features: {
      均值: true,
      方差: true,
      标准差: true,
      峰度: true,
      偏度: true,
      四阶累积量: true,
      六阶累积量: true,
      最大值: true,
      最小值: true,
      中位数: true,
      峰峰值: true,
      整流平均值: true,
      均方根: true,
      方根幅值: true,
      波形因子: true,
      峰值因子: true,
      脉冲因子: true,
      裕度因子: true,
      重心频率: true,
      均方频率: true,
      均方根频率: true,
      频率方差: true,
      频率标准差: true,
      谱峭度的均值: true,
      谱峭度的峰度: true,
    },
    correlation_coefficient_importance: {'rule': 1, 'threshold1': 0.25, 'threshold2': 0.1},
    private_fault_diagnosis_machine_learning: '',
  },
  schedule: ["数据源", "特征提取", "特征选择", "故障诊断"],
  mutipleSensor: false,
};

// 校验故障预测新增服务组件
let contentJsonForFaultPrediction = {
  modules: ["故障诊断", "特征提取", "特征选择"],
  algorithms: {
    特征提取: "time_frequency_domain_features",
    特征选择: "correlation_coefficient_importance",
    故障诊断: "random_forest_machine_learning",
    故障预测: "private_fault_prediction",
  },
  parameters: {
    time_frequency_domain_features: {
      均值: true,
      方差: true,
      标准差: true,
      峰度: true,
      偏度: true,
      四阶累积量: true,
      六阶累积量: true,
      最大值: true,
      最小值: true,
      中位数: true,
      峰峰值: true,
      整流平均值: true,
      均方根: true,
      方根幅值: true,
      波形因子: true,
      峰值因子: true,
      脉冲因子: true,
      裕度因子: true,
      重心频率: true,
      均方频率: true,
      均方根频率: true,
      频率方差: true,
      频率标准差: true,
      谱峭度的均值: true,
      谱峭度的峰度: true,
    },
    correlation_coefficient_importance: {'rule': 1, 'threshold1': 0.25, 'threshold2': 0.1},
    random_forest_machine_learning: {},
    private_fault_prediction: '',
  },
  schedule: ["数据源", "特征提取", "特征选择", "故障诊断", "故障预测"],
  mutipleSensor: false,
};

// 校验健康评估增值服务组件
let contentJsonForHealthEvaluation = {
  modules: ["特征提取", "健康评估"],
  algorithms: { 
    特征提取: "time_frequency_domain_features",
    健康评估: "private_health_evaluation",
  },
  parameters: { 
    time_frequency_domain_features: {
      均值: true,
      方差: true,
      标准差: true,
      峰度: true,
      偏度: true,
      四阶累积量: true,
      六阶累积量: true,
      最大值: true,
      最小值: true,
      中位数: true,
      峰峰值: true,
      整流平均值: true,
      均方根: true,
      方根幅值: true,
      波形因子: true,
      峰值因子: true,
      脉冲因子: true,
      裕度因子: true,
      重心频率: true,
      均方频率: true,
      均方根频率: true,
      频率方差: true,
      频率标准差: true,
      谱峭度的均值: true,
      谱峭度的峰度: true,
    },
    private_health_evaluation: "" 
  },
  schedule: ["数据源", "特征提取", "健康评估"],
  multipleSensor: false, // 是否为多传感器数据
}

// 校验小波变换增值组件
// let contentJsonForWaveletTrans = {
//   modules: ["小波变换"],
//   algorithms: { 小波变换: "extra_wavelet_transform" },
//   parameters: { extra_wavelet_transform: "" },
//   schedule: ["数据源", "小波变换"],
//   multipleSensor: false, // 是否为多传感器数据
// };

// const validateExtraModuleUsingFileName = ref('')
// 增值服务组件完整性校验结果
const extraModuleValidationResult = ref(false);
const canShowValidationResult = ref(false);


let validationResultsToDisplay: Object;
//上传文件后，点击开始运行以运行程序
const startValidating = () => {
  const data = new FormData();
  // data.append("file_name", validateExtraAlgorithmUsingFileName.value); // 所使用的数据文件
  data.append("params", JSON.stringify(contentJson)); // 需要进行组件校验时的默认校验模型
  let algorithmType = uploadAlgorithmForm.algorithmType;

  switch (algorithmType) {
    case "插值处理":
      data.append("validationExample", "example_for_interpolation_validation");
      break;
    case "小波变换":
      data.append("validationExample", "single_sensor_example");
      break;
    case "无量纲化":
      data.append("validationExample", "single_sensor_example");
      break;
    case "健康评估":
      data.append("validationExample", "example_for_fault_diagnosis_validation");
      break;
    case "故障预测":
    case "故障诊断":
      if (uploadAlgorithmForm.faultDiagnosisType === "machineLearning") {
        data.append("validationExample", "example_for_fault_diagnosis_validation");
      } else {
        data.append("validationExample", "example_for_fault_diagnosis_validation_multiple");
      }
      break;
    default:
      data.append("validationExample", "single_sensor_example");
  }

  // data.append('validationExample', 'single_sensor_example')

  return api
    .post("user/run_with_datafile_on_cloud/", data, {
      headers: { "Content-Type": "multipart/form-data" },
    })
    .then((response: any) => {
      if (response.data.code == 401) {
        ElMessageBox.alert("登录状态已失效，请重新登陆", "提示", {
          confirmButtonText: "确定",
          callback: () => {
            router.push("/");
          },
        });
      }
      if (response.data.code === 200) {
        message.success("组件校验成功！");
        validationResultsToDisplay = response.data.results
        extraModuleValidationResult.value = true;
        emit('addExtraModule')
      } else {
        extraModuleValidationResult.value = false;
        message.error("组件校验失败，" + response.data.message);
      }
      uploading.value = false;
    })
    .catch((error: any) => {
      if (error.response) {
        // 请求已发出，服务器响应了状态码，但不在2xx范围内
        console.log(error.response.status); // HTTP状态码
        console.log(error.response.statusText); // 状态消息
      } else if (error.request) {
        // 请求已发起，但没有收到响应
        console.log(error.request);
      } else {
        // 设置请求时触发了错误
        console.error("Error", error.message);
      }
      uploading.value = false;
      extraModuleValidationResult.value = false;
      message.error("校验程序运行出错，请检查上传的文件是否符合模板规范");
    });
};


// 如果校验失败则需要删除上传的增值服务组件
const deleteExtraModule = () => {
  // 发送删除请求到后端，row 是要删除的数据行
  api
    .get(
      "/user/delete_extra_algorithm/?algorithmAlias=" +
        extraAlgorithmFileFormState.algorithmName
    )
    .then((response: any) => {
      if (response.data.code == 401) {
        ElMessageBox.alert("登录状态失效，请重新登陆", "提示", {
          confirmButtonText: "确定",
          callback: () => {
            router.push("/");
          },
        });
      }
      if (response.data.code == 200) {
        console.log("组件已删除成功");
      } else {
        console.log("删除组件失败，请稍后重试");
        // if (response.data.code == 404) {
        //   ElMessage({
        //     message: "没有权限删除该组件",
        //     type: "error",
        //   });
        // } else {
        //   ElMessage({
        //     message: "删除组件失败，请稍后重试",
        //     type: "error",
        //   });
        // }
      }
    })
    .catch((error: any) => {
      // 处理错误
      console.error(error);
      // ElMessage({
      //   message: "删除组件失败," + error,
      //   type: "error",
      // });
    });
};

const canDisplayInterpolationValidationResult = ref(false)  // 插值处理组件校验结果
const canDisplayWaveletTransformValidationResult = ref(false)  // 小波变换组件校验结果
const canDisplayDimensionlessValidationResult = ref(false)  // 无量纲化组件校验结果
const canDisplayFaultDiagnosisValidationResult = ref(false)  // 故障诊断组件校验结果
const canDisplayHealthEvaluationValidationResult = ref(false)  // 健康评估组件校验结果
const canDisplayFaultPredictionValidationResult = ref(false)  // 故障预测组件校验结果

const resetDisplay = () => {
  canDisplayInterpolationValidationResult.value = false
  canDisplayWaveletTransformValidationResult.value = false
  canDisplayDimensionlessValidationResult.value = false
  canDisplayFaultDiagnosisValidationResult.value = false
  canDisplayHealthEvaluationValidationResult.value = false
  canDisplayFaultPredictionValidationResult.value = false
}

// 关闭组件校验结果
const closeValidationResult = () => {
  canShowValidationResult.value = false
}

const interpolationFigures = ref<string[]>([])  // 插值处理组件校验结果
const waveletTransformFigures = ref<string[]>([])  // 小波变换组件校验结果
const dimensionlessFigures = ref<string[]>([])  // 无量纲化组件校验结果
const faultDiagnosisFigures = ref<string[]>([])  // 故障诊断组件校验结果
const healthEvaluationFigures = ref<string[]>([])  // 健康评估组件校验结果
const faultPredictionFigures = ref<string[]>([])  // 故障预测组件校验结果
// const interpolationResultsOfSensors = ref([])
interface ResultsObject {  // 完整性校验结果
  插值处理: Object
  小波变换: Object
  无量纲化: Object
  故障诊断: Object
}

// 完整性校验通过后的结果展示
const displayValidationResult = (algorithmType: string, resultsObject: ResultsObject) => {
  interpolationFigures.value.length = 0
  // interpolationResultsOfSensors.value.length = 0
  // 清除显示结果
  resetDisplay();  
  if (algorithmType == "插值处理"){
    canDisplayInterpolationValidationResult.value = true
    for(const [key, value] of Object.entries(resultsObject.插值处理)){
      // 将插值处理的结果添加到插值图展示
      // console.log('value: ', value)
      interpolationFigures.value.push('data:image/png;base64,' + value)
      // interpolationResultsOfSensors.value.push({label: key.split('_')[0], name: sensorId.toString()})
    }
  }else if(algorithmType == "无量纲化"){
    canDisplayDimensionlessValidationResult.value = true
    for(const [key, value] of Object.entries(resultsObject.无量纲化)){
      // interpolationFigures.value.push('data:image/png;base64,' + value)
      dimensionlessFigures.value.push('data:image/png;base64,' + value)
    }
  }else if(algorithmType == "故障诊断"){
    canDisplayFaultDiagnosisValidationResult.value = true
    let faultDiagnosisValidationResult: string = resultsObject.故障诊断.fd_validation_result
    // interpolationFigures.value.push('data:image/png;base64,' + value)
    faultDiagnosisFigures.value.push('data:image/png;base64,' + faultDiagnosisValidationResult)
    
  }else if(algorithmType == "健康评估"){
    canDisplayHealthEvaluationValidationResult.value = true
    let healthEvaluationValidationResult: string = resultsObject.健康评估.he_validation_result
    healthEvaluationFigures.value.push('data:image/png;base64,' + healthEvaluationValidationResult)
  }
  else if (algorithmType == "小波变换"){
    canDisplayWaveletTransformValidationResult.value = true
    // interpolationFigures.value.push('data:image/png;base64,' + resultsObject.小波变换)
    for(const [key, value] of Object.entries(resultsObject.小波变换)){
      waveletTransformFigures.value.push('data:image/png;base64,' + value)
    }
  }
  else if (algorithmType == "故障预测"){
    canDisplayFaultPredictionValidationResult.value = true
    // interpolationFigures.value.push('data:image/png;base64,' + resultsObject.小波变换)
    for(const [key, value] of Object.entries(resultsObject.故障预测)){
      faultPredictionFigures.value.push('data:image/png;base64,' + value)
    }
  }

  
}


// 校验增值服务组件所使用的用户样本
const validateExtraAlgorithmUsingFileName = ref("");

// 提交上传组件并进行校验
const extraModuleUploadAndValidate = async () => {
  // extraModuleValidationResult.value = true
  // 首先上传增值服务组件然后进行校验，校验通过再保存上传的结果
  try {
    await uploadExtraModuleWithName();
    console.log("上传成功");
    // 进行后续操作
  } catch (error) {
    console.error("上传失败:", error);
    // message.error("组件上传失败");
    return;
  }
  let algorithmName = extraAlgorithmFileFormState.algorithmName;
  if (uploadAlgorithmForm.algorithmType == "小波变换") {
    contentJsonForWaveletTrans.parameters["extra_wavelet_transform"] = algorithmName;
    // 将contentJsonForWaveletTrans的值复制给contentJson
    Object.assign(contentJson, contentJsonForWaveletTrans);
  } else if (uploadAlgorithmForm.algorithmType == "插值处理") {
    contentJsonForInterpolation.parameters["private_interpolation"] = algorithmName;
    Object.assign(contentJson, contentJsonForInterpolation);
  } else if (uploadAlgorithmForm.algorithmType == "无量纲化") {
    contentJsonForDimensionless.parameters["private_scaler"]["algorithm"] = algorithmName;
    contentJsonForDimensionless.parameters["private_scaler"]["useLog"] = uploadAlgorithmForm.useLog;
    Object.assign(contentJson, contentJsonForDimensionless);
  } else if (uploadAlgorithmForm.algorithmType == '故障诊断') {
    if (uploadAlgorithmForm.faultDiagnosisType == 'machineLearning'){
      // 基于机器学习的故障诊断的组件校验
      contentJsonForFaultDiagnosisML.parameters['private_fault_diagnosis_machine_learning'] = algorithmName;
      Object.assign(contentJson, contentJsonForFaultDiagnosisML)
    }
    if (uploadAlgorithmForm.faultDiagnosisType == 'deepLearning'){
      // 基于深度学习的故障诊断的组件校验
      contentJsonForFaultDiagnosisDL.parameters['private_fault_diagnosis_deeplearning'] = algorithmName;
      Object.assign(contentJson, contentJsonForFaultDiagnosisDL)
    }
  } else if (uploadAlgorithmForm.algorithmType == '健康评估'){
    contentJsonForHealthEvaluation.parameters['private_health_evaluation'] = algorithmName;
    Object.assign(contentJson, contentJsonForHealthEvaluation)
  } else if(uploadAlgorithmForm.algorithmType == '故障预测'){
    contentJsonForFaultPrediction.parameters['private_fault_prediction'] = algorithmName;
    Object.assign(contentJson, contentJsonForFaultPrediction)
  } else {
    // message.error("上传增值服务组件失败，请检查算法类型是否正确");
    return;
  }
  // emit("validateExtraModule", {
  //   contentJson: contentJson,
  //   usingFileName: validateExtraAlgorithmUsingFileName.value,
  // });
  try {
    // 运行校验程序进行完整性校验
    await startValidating();
    canShowValidationResult.value = true;
    if (extraModuleValidationResult.value === true) {
      displayValidationResult(uploadAlgorithmForm.algorithmType, validationResultsToDisplay)
      // message.success("组件校验通过");
    } else {
      // 组件校验失败，删除已上传的组件
      deleteExtraModule();
      // message.error("组件校验失败");
      // removeModelFile(algorithmName);
    }
  } catch (error) {
    message.error("校验过程中发生错误");
    // message.error("校验失败");
  }
};

// const uploadExtraModuleWithName = () => {
//   // console.log("algorithmFileFormState.value", algorithmFileFormState.value);
//   algorithmFileFormRef.value
//     .validate()
//     .then(() => {
//       // 上传算法组件
//       let formData = new FormData();
//       // formData.append("algorithmFile", algorithmFileFormState.value.algorithmFile);
//       formData.append("algorithmName", algorithmFileFormState.algorithmName);
//       formData.append("statement", algorithmFileFormState.statement);
//       //   // 发送文件上传请求
//       formData.append("algorithm_type", unknownform.algorithmType);
//       formData.append("faultDiagnosisType", unknownform.faultDiagnosisType);

//       // 将pythonFileList和modelFileList中的文件添加到formData中
//       for (let i = 0; i < pythonFileList.value.length; i++) {
//         formData.append("algorithmFile", pythonFileList.value[i]);
//       }
//       for (let i = 0; i < modelFileList.value.length; i++) {
//         formData.append("modelParamsFile", modelFileList.value[i]);
//       }
//       return api
//         .post("/user/upload_user_private_algorithm/", formData)
//         .then((response: any) => {
//           if (response.data.code == 200) {
//             pythonFileList.value = [];
//             modelFileList.value = [];
//             message.success("算法文件上传成功");
//             dialogVisible.value = true;
//             ruleOfFDA = 0;
//             // 进行算法组件完整性的校验
//           } else {
//             uploading.value = false;
//             message.error("算法文件上传失败, " + response.data.message);
//           }
//           if (response.data.code == 401) {
//             ElMessageBox.alert("登录状态已失效，请重新登陆", "提示", {
//               confirmButtonText: "确定",
//               callback: (action: Action) => {
//                 router.push("/");
//               },
//             });
//           }
//         })
//         .catch((error: any) => {
//           uploading.value = false;
//           message.error("上传失败, 请重试");
//         });
//       //
//     })
//     .catch((error) => {
//       console.log("error", error);
//       message.error("请填写完整的组件信息");
//       return false;
//     });
// };

const uploadExtraModuleWithName = () => {
  return new Promise((resolve, reject) => {
    algorithmFileFormRef.value
      .validate()
      .then(() => {
        // 上传算法组件
        let formData = new FormData();
        formData.append("algorithmName", extraAlgorithmFileFormState.algorithmName);
        formData.append("statement", extraAlgorithmFileFormState.statement);
        formData.append("algorithm_type", uploadAlgorithmForm.algorithmType);
        formData.append("faultDiagnosisType", uploadAlgorithmForm.faultDiagnosisType);

        // 将pythonFileList和modelFileList中的文件添加到formData中
        for (let i = 0; i < pythonFileList.value.length; i++) {
          formData.append("algorithmFile", pythonFileList.value[i]);
        }
        for (let i = 0; i < modelFileList.value.length; i++) {
          formData.append("modelParamsFile", modelFileList.value[i]);
        }
        uploading.value = true;
        return api
          .post("/user/upload_user_private_algorithm/", formData)
          .then((response) => {
            if (response.data.code == 200) {
              pythonFileList.value = [];
              modelFileList.value = [];
              message.success("算法文件上传成功");
              dialogVisible.value = true;
              ruleOfFDA = 0;
              // 进行算法组件完整性的校验
              resolve(true); // 成功上传，resolve
            } else {
              uploading.value = false;
              message.error("算法文件上传失败, " + response.data.message);
              reject(new Error("上传失败: " + response.data.message)); // 失败，reject
            }
            if (response.data.code == 401) {
              ElMessageBox.alert("登录状态已失效，请重新登陆", "提示", {
                confirmButtonText: "确定",
                callback: (action) => {
                  router.push("/");
                },
              });
            }
          })
          .catch((error) => {
            uploading.value = false;
            message.error("上传失败, 请重试");
            reject(error); // 捕获错误，reject
          });
      })
      .catch((error) => {
        console.log("error", error);
        message.error("请填写完整的组件信息");
        reject(new Error("验证失败: 请填写完整的组件信息")); // 验证失败，reject
      });
  });
};
const removePythonFile: UploadProps["onRemove"] = (file) => {
  // 在删除文件列表中文件的同时，重新计算ruleOfDFA，以保证用户上传私有故障诊断算法时，同时包含用于故障诊断的模型以及模型参数文件。
  const isFaultDiagnosis = uploadAlgorithmForm.algorithmType === "故障诊断";
  const isFaultPrediction = uploadAlgorithmForm.algorithmType === "故障预测";
  const isNormalization = uploadAlgorithmForm.algorithmType === "无量纲化";
  const isHealthEvaluation = uploadAlgorithmForm.algorithmType === "健康评估";
  const isPyFile = file.type === "application/x-python-code" || file.name.endsWith(".py");
  const isPklFile = file.name.endsWith(".pkl");
  const isPthFile = file.name.endsWith(".pth");
  // 当用户选择上传故障诊断或是故障预测算法时，如果删除了python文件，则ruleOfDFA减1；如果删除了模型参数文件，则ruleOfDFA加1
  if (isFaultDiagnosis || isFaultPrediction) {
    if (isPyFile && ruleOfFDA > -1) ruleOfFDA -= 1;
    if ((isPklFile || isPthFile) && ruleOfFDA < 1) ruleOfFDA += 1;
  }
  // 当用户选择上传无量纲化算法时，如果删除了python文件，则ruleOfNor减1；如果删除了模型参数文件，则ruleOfNor加1
  if (isNormalization) {
    if (isPyFile && ruleOfNor > -1) ruleOfNor -= 1;
    if ((isPklFile || isPthFile) && ruleOfNor < 1) ruleOfNor += 1;
  }
  // 当用户选择上传健康评估算法时，如果删除了python文件，则ruleOfHev减1；如果删除了模型参数文件，则ruleOfHev加1
  if (isHealthEvaluation) {
    if (isPyFile && ruleOfHev > -1) ruleOfHev -= 1;
    if ((isPklFile || isPthFile) && ruleOfHev < 1) ruleOfHev += 1;
  }
  // 删除文件列表中用户上传的文件
  if (pythonFileList.value) {
    const index = pythonFileList.value.indexOf(file);
    const newFileList = pythonFileList.value.slice();
    newFileList.splice(index, 1);
    pythonFileList.value = newFileList;
  } else {
    console.log("fileList is undefined");
  }
};

const algorithmTypeChange = (value: string, label: any, extra: any) => {
  // 当用户选择算法类型时，清空文件列表
  console.log("value: ", value);
  selectAlgorithmType();
  canSelectPythonFile.value = false;
  // 当用户选择算法类型时，判断是否可以上传模型文件
  if (
    value === "故障诊断" ||
    value === "故障预测" ||
    value === "健康评估" ||
    value === "无量纲化"
  ) {
    if (value === "无量纲化") {
      if (!uploadAlgorithmForm.useLog) {
        canUploadModelFile.value = false;
      }
      return;
    }
    canUploadModelFile.value = true;
  } else {
    canUploadModelFile.value = false;
  }
};

// 当用户选择算法类型时，清空文件列表
const selectAlgorithmType = () => {
  if (pythonFileList.value) {
    pythonFileList.value.forEach((file) => {
      removePythonFile(file);
    });
  }
};

// 算法类型为树形选择器
// const algorithmType = ref();
const treeData = ref([
  {
    label: "预处理组件",
    value: "预处理组件",
    selectable: false,
    children: [
      {
        label: "插值处理",
        value: "插值处理",
      },
      // {
      //   label: "特征提取",
      //   value: "特征提取",
      // },
      {
        label: "小波变换",
        value: "小波变换",
      },
      // {
      //   label: "特征选择",
      //   value: "特征选择",
      // },
      {
        label: "无量纲化",
        value: "无量纲化",
      },
    ],
  },
  {
    label: "故障检测组件",
    value: "故障检测组件",
    selectable: false,
    children: [
      {
        label: "故障诊断",
        value: "故障诊断",
      },
      {
        label: "故障预测",
        value: "故障预测",
      },
    ],
  },
  {
    label: "健康评估组件",
    value: "健康评估组件",
    selectable: false,
    children: [
      {
        label: "健康评估",
        value: "健康评估",
      },
    ],
  },
]);

//根据用户选择上传的私有算法的类型设置文件上传数量
const fileCount = ref(1);

let ruleOfFDA = 0;
let ruleOfNor = 0;
let ruleOfHev = 0;

const beforeUploadAlgorithmFile = (file: any) => {
  // 判断传入的文件类型是否为python文件，限定用户只能上传python文件
  const isPyFile = file.type === "application/x-python-code" || file.name.endsWith(".py");
  if (!isPyFile) {
    message.warning("请上传包含该算法的python文件");
    return;
  } else {
    let fileNum = pythonFileList.value?.length;
    if (fileNum == 1) {
      if (isPyFile) {
        removePythonFile(file);
        pythonFileList.value = [...(pythonFileList.value || []), file]; //将文件添加到fileList中
        message.warning("最多只能上传一个.py类型的文件");
        return false;
      }
      message.warn("上传该类型算法时，最多只能上传一个.py类型的文件");
      return false;
    }
    // 将文件加入到文件列表
    pythonFileList.value = [...(pythonFileList.value || []), file]; //将文件添加到fileList中
    return false;
  }
};

// 删除模型文件
const removeModelFile: UploadProps["onRemove"] = (file) => {
  console.log("file: ", file);
  // 删除文件列表中用户上传的文件
  if (modelFileList.value) {
    const index = modelFileList.value.indexOf(file);
    const newFileList = modelFileList.value.slice();
    newFileList.splice(index, 1);
    modelFileList.value = newFileList;
  } else {
    console.log("fileList is undefined");
  }
};

// 上传模型文件
const canUploadModelFile = ref(false);
const beforeUploadModelFile = (file: any) => {
  let isFaultDiagnosis = uploadAlgorithmForm.algorithmType === "故障诊断" ? true : false;
  let isHealthEvaluation = uploadAlgorithmForm.algorithmType === "健康评估" ? true : false;
  let isNormalization = uploadAlgorithmForm.algorithmType === "无量纲化" ? true : false;
  let uploadModelFileType;
  let isPklFile = file.name.endsWith(".pkl");
  let isPthFile = file.name.endsWith(".pth");
  let faultDiagnosisType;
  if (isFaultDiagnosis) {
    // 如果上传故障诊断组件，如果是机器学习的故障诊断，需要上传.pkl的文件，深度学习的故障诊断需要上传.pth的文件
    faultDiagnosisType = uploadAlgorithmForm.faultDiagnosisType;
    if (faultDiagnosisType === "machineLearning") {
      if (!isPklFile) {
        message.warning("上传基于机器学习的算法，请上传.pkl的模型文件");
        return false;
      }
      uploadModelFileType = "pkl";
    } else {
      if (!isPthFile) {
        message.warning("上传基于深度学习的算法，请上传.pth的模型文件");
        return false;
      }
      uploadModelFileType = "pth";
    }
  }

  if (isHealthEvaluation) {
    if (!isPklFile) {
      message.warning("上传健康评估算法，请上传.pkl的模型文件");
      return false;
    }
  }

  if (isNormalization) {
    if (uploadAlgorithmForm.useLog) {
      if (!isPklFile) {
        message.warning("上传对于所提取特征的无量纲化算法，请上传.pkl的模型文件");
        return false;
      }
    }
  }

  let fileNum = modelFileList.value?.length;
  if (fileNum == 1) {
    if (uploadModelFileType === "pkl") {
      if (isPklFile) {
        removeModelFile(file);
        modelFileList.value = [...(modelFileList.value || []), file]; //将文件添加到fileList中
        message.warning("最多只能上传一个.pkl类型的模型文件");
        return false;
      }
      message.warn("上传该类型算法时，最多只能上传一个.pkl类型的文件");
      return false;
    } else {
      if (isPthFile) {
        removeModelFile(file);
        modelFileList.value = [...(modelFileList.value || []), file]; //将文件添加到fileList中
        message.warning("最多只能上传一个.pth类型的模型文件");
        return false;
      }
      message.warn("上传该类型算法时，最多只能上传一个.pth类型的文件");
      return false;
    }
  }

  // 将文件添加到modelFileList中
  modelFileList.value = [...(modelFileList.value || []), file];
  return false;
};



// const beforeUpload = (file: any) => {
//   const algorithmType = form.value.algorithmType;
//   const isFaultDiagnosis = algorithmType === "故障诊断";
//   const isFaultPrediction = algorithmType === "故障预测";
//   const isNormalization = algorithmType === "无量纲化";
//   const isHealthEvaluation = algorithmType === "健康评估";
//   const isPyFile = file.type === "application/x-python-code" || file.name.endsWith(".py");
//   const isPklFile = file.name.endsWith(".pkl");
//   const isPthFile = file.name.endsWith(".pth");

//   let fileNum = pythonFileList.value?.length;
//   if (fileNum == 0) {
//     ruleOfFDA = 0;
//     ruleOfNor = 0;
//     ruleOfHev = 0;
//   }
//   // 对于上传私有故障诊断、故障预测算法、健康评估算法的规则判断
//   if (isFaultDiagnosis || isFaultPrediction || isHealthEvaluation) {
//     // 判断用户上传的私有算法文件是否是python文件
//     if (fileNum == 0 && !isPyFile && !isPklFile && !isPthFile) {
//       message.error(
//         "请上传包含该" +
//           algorithmType +
//           "算法(.py类型)或是模型参数(.pth或是.pkl类型)的文件"
//       );
//       return false;
//     }
//     //判断是否是用户上传私有算法时是否同时上传了故障诊断的模型以及相关的模型参数文件（共两个文件）
//     if (fileNum == 1) {
//       if (
//         !(isPyFile && ruleOfFDA == -1) &&
//         !((isPthFile || isPklFile) && ruleOfFDA == 1) &&
//         !(isPyFile && ruleOfHev == -1) &&
//         !(isPklFile && ruleOfHev == 1)
//       ) {
//         message.error(
//           "上传" +
//             algorithmType +
//             "算法时，需要上传定义的" +
//             algorithmType +
//             "算法(.py文件)以及诊断时使用的模型的加载参数(.pkl或.pth文件)"
//         );
//         return false;
//       }
//     }

//     if (fileNum == 2) {
//       message.error(
//         "上传" + algorithmType + "算法时，最多只能上传包含该算法的源文件和模型参数文件"
//       );
//       return false;
//     }
//   } else if (isNormalization) {
//     // 对于上传无量纲化算法的规则判断
//     const useLog = form.value.useLog; // 为true时，对原始信号进行标准化，为false时，对提取到的特征进行标准化

//     if (!useLog) {
//       // 对原始信号进行无量纲化
//       if (fileNum == 0 && !isPyFile) {
//         message.error("请上传包含该算法的.py类型的文件");
//         return false;
//       } else {
//         // 当选择上传无量纲化私有算法时，文件列表中最多只能有一个py文件
//         if (fileNum == 1) {
//           if (isPyFile) {
//             handleRemove(file);
//           } else {
//             message.error("上传无量纲化算法时，最多只能上传一个包含该算法的python源文件");
//             return false;
//           }
//         }
//       }
//     } else {
//       // 对提取到的特征进行无量纲化
//       // 判断用户上传的私有算法文件是否是python文件
//       if (fileNum == 0 && !isPyFile && !isPklFile) {
//         message.error(
//           "请上传包含该" + algorithmType + "算法(.py类型)或是模型参数(pkl类型)的文件"
//         );
//         return false;
//       }
//       //判断是否是用户上传保存了训练数据参数的无量纲化算法时是否同时上传了无量纲化算法以及相关的模型文件（共两个文件）
//       if (fileNum == 1) {
//         if (!(isPyFile && ruleOfNor == -1) && !(isPklFile && ruleOfNor == 1)) {
//           message.error(
//             "上传" +
//               algorithmType +
//               "算法时，需要上传定义的" +
//               algorithmType +
//               "算法(.py文件)以及诊断时使用的模型的加载参数(.pkl文件)"
//           );
//           return false;
//         }
//       }
//       if (fileNum == 2) {
//         message.error(
//           "上传" + algorithmType + "算法时，最多只能上传包含该算法的源文件和模型参数文件"
//         );
//         return false;
//       }
//     }
//   } else {
//     if (fileNum == 0 && !isPyFile) {
//       message.error("请上传包含该算法的.py类型的文件");
//       return false;
//     }
//     // 当选择上传除故障诊断、故障预测、健康评估算法的其他专有算法时，文件列表中最多只能有一个py文件
//     if (fileNum == 1) {
//       if (isPyFile) {
//         handleRemove(file);
//         pythonFileList.value = [...(pythonFileList.value || []), file]; //将文件添加到fileList中
//         return false;
//       }
//   // 用于判断是否是用户上传的私有故障诊断算法时是否同时上传了故障诊断的模型以及相关的模型参数文件
//   if ((isFaultDiagnosis || isFaultPrediction) && isPyFile) {
//     ruleOfFDA += 1;
//   }
//   if ((isFaultDiagnosis || isFaultPrediction) && (isPklFile || isPthFile)) {
//     ruleOfFDA -= 1;
//   }

//   // 用于判断用户上传的模型训练时的无量纲化算法是否同时上传了无量纲算法以及相关的模型文件
//   if (isNormalization) {
//     if (isPyFile) ruleOfNor += 1;
//     if (isPklFile || isPthFile) ruleOfNor -= 1;
//   }

//   // 用于判断用户上传的健康评估算法是否同时上传了健康评估算法以及相关的模型文件
//   if (isHealthEvaluation) {
//     if (isPyFile) ruleOfHev += 1;
//     if (isPklFile) ruleOfHev -= 1;
//   }
//   // if (isNormalization && (isPklFile || isPthFile)){
//   //   ruleOfNor -= 1;
//   // }
//   // console.log('beforeUpload: ', ruleOfFDA)
//   // console.log('beforeUpload: ', ruleOfFDA)
//   return false; // 阻止默认上传行为
// };

// const uploadExtraModule = () => {
//   if (!form.value.algorithmType) {
//     message.error("请选择算法类型");
//     return;
//   }
//   let isFaultDiagnosis = form.value.algorithmType === "故障诊断" ? true : false;
//   const formData = new FormData();
//   // fileList.value.forEach((file: UploadProps['fileList'][number]) => {
//   //   formData.append('files[]', file as any);
//   // });
//   let fileNum = pythonFileList.value?.length;

//   if (fileNum == 0) {
//     message.error("请选择上传包含算法的源文件");
//     return;
//   }

//   if (fileNum == 1) {
//     let algorithmType = form.value.algorithmType;
//     if (
//       algorithmType != "故障诊断" &&
//       algorithmType != "故障预测" &&
//       !(algorithmType == "无量纲化" && form.value.useLog) &&
//       algorithmType != "健康评估"
//     ) {
//       //上传除了故障诊断、故障预测、健康评估、保存训练数据参数的无量纲化以外的算法时，只能上传一个包含该算法的python源文件
//       if (pythonFileList.value) {
//         let isPyFile = pythonFileList.value[0].name.endsWith(".py");
//         if (!isPyFile) {
//           message.error("请选择上传包含该算法的py源文件");
//           return;
//         }
//         let file = pythonFileList.value[0];
//         formData.append("algorithmFile", file);
//       }
//     } else {
//       //上传专有故障诊断、专有故障预测算法、专有健康评估算法、记录训练数据参数的专有无量纲化算法时，需要同时包含定义算法文件与模型参数文件
//       if (pythonFileList.value) {
//         let isPyFile = pythonFileList.value[0].name.endsWith(".py");
//         let isPklFile = pythonFileList.value[0].name.endsWith(".pkl");
//         let isPthFile = pythonFileList.value[0].name.endsWith(".pth");
//         if (isPyFile) {
//           if (algorithmType == "无量纲化" && form.value.useLog) {
//             message.error(
//               "如果上传保存了训练数据参数的无量纲化方法，则需要同时上传模型文件(.pkl类型)"
//             );
//             return;
//           }

//           if (isFaultDiagnosis) {
//             let isMachineLearning =
//               form.value.faultDiagnosisType === "machineLearning" ? true : false;
//             if (isMachineLearning) {
//               message.error(
//                 '上传基于机器学习的故障诊断算法时，需上传模型".pkl类型"的模型文件'
//               );
//             } else {
//               message.error(
//                 '上传基于深度学习的故障诊断算法时，需上传模型".pth类型"的模型文件'
//               );
//             }
//             return;
//           }
//         }

//         if (isPklFile || isPthFile) {
//           message.error(
//             "上传" +
//               algorithmType +
//               "算法时，需上传定义的" +
//               algorithmType +
//               "算法(.py类型)"
//           );
//           return;
//         }
//       }
//     }
//   } else {
//     if (!isFaultDiagnosis) {
//       message.error("上传非故障诊断的算法时，仅需要上传一个包含该算法的py源文件");
//       return;
//     }
//     //上传私有故障诊断算法
//     let algorithm;
//     let modelParams;
//     if (pythonFileList.value && fileNum) {
//       for (let i = 0; i < fileNum; i++) {
//         if (pythonFileList.value[i].name.endsWith(".py")) {
//           formData.append("algorithmFile", pythonFileList.value[i]);
//           algorithm = pythonFileList.value[i].name.split(".")[0];
//         } else {
//           formData.append("modelParamsFile", pythonFileList.value[i]);
//           modelParams = pythonFileList.value[i].name.split(".")[0];
//         }
//       }
//       if (algorithm !== modelParams) {
//         let algorithmType = form.value.algorithmType;

//         message.error(
//           "上传定义的" +
//             algorithmType +
//             "算法(.py文件)以及使用的模型的加载参数(.pkl或.pth文件)时，两个文件名称需要保持一致"
//         );
//         return;
//       }
//     }
//   }

//   formData.append("algorithm_type", form.value.algorithmType);
//   formData.append("faultDiagnosisType", form.value.faultDiagnosisType);

//   uploading.value = true;

//   api
//     .post("/user/upload_user_private_algorithm/", formData)
//     .then((response: any) => {
//       if (response.data.code == 200) {
//         pythonFileList.value = [];
//         uploading.value = false;
//         message.success("算法文件上传成功");
//         dialogVisible.value = true;
//         ruleOfFDA = 0;
//       } else {
//         uploading.value = false;
//         message.error("算法文件上传失败, " + response.data.message);
//       }
//       if (response.data.code == 401) {
//         ElMessageBox.alert("登录状态已失效，请重新登陆", "提示", {
//           confirmButtonText: "确定",
//           callback: (action: Action) => {
//             router.push("/");
//           },
//         });
//       }
//     })
//     .catch((error: any) => {
//       uploading.value = false;
//       message.error("上传失败, 请重试");
//     });
// };    message.warn("上传该类型算法时，最多只能上传一个.py类型的文件");
//       return false;
//     }
//   }

//   pythonFileList.value = [...(pythonFileList.value || []), file]; //将文件添加到fileList中
//

// const uploadExtraModule = () => {
//   let isFaultDiagnosis = form.value.algorithmType == "故障诊断" ? true : false;
//   let isHealthEvaluation = form.value.algorithmType == "健康评估" ? true : false;
//   let isFaultPrediction = form.value.algorithmType == "故障预测" ? true : false;
//   let scalerForFeatures =
//     form.value.algorithmType == "无量纲化" && form.value.useLog ? true : false;

//   let pythonFileName = pythonFileList.value[0].name.split(".")[0];
//   if (isFaultDiagnosis || isHealthEvaluation || isFaultPrediction || scalerForFeatures) {
//     let modelFileName = modelFileList.value[0].name.split(".")[0];
//     if (pythonFileName !== modelFileName) {
//       let algorithmType = form.value.algorithmType;
//       message.error(
//         "上传定义的" +
//           algorithmType +
//           "算法(.py文件)以及使用的模型的加载参数(.pkl或.pth文件)时，两个文件名称需要保持一致"
//       );
//       return;
//     }
//   }

//   let formData = new FormData();
//   // 发送文件上传请求
//   formData.append("algorithm_type", form.value.algorithmType);
//   formData.append("faultDiagnosisType", form.value.faultDiagnosisType);

//   // 将pythonFileList和modelFileList中的文件添加到formData中
//   for (let i = 0; i < pythonFileList.value.length; i++) {
//     formData.append("algorithmFile", pythonFileList.value[i]);
//   }
//   for (let i = 0; i < modelFileList.value.length; i++) {
//     formData.append("modelParamsFile", modelFileList.value[i]);
//   }

//   uploading.value = true;
//   // algorithmFileFormRef.value.validate().then(() => {
//   //   uploadExtraModule();
//   // });
//   api
//     .post("/user/upload_user_private_algorithm/", formData)
//     .then((response: any) => {
//       if (response.data.code == 200) {
//         pythonFileList.value = [];
//         modelFileList.value = [];
//         uploading.value = false;
//         message.success("算法文件上传成功");
//         dialogVisible.value = true;
//         ruleOfFDA = 0;
//       } else {
//         uploading.value = false;
//         message.error("算法文件上传失败, " + response.data.message);
//       }
//       if (response.data.code == 401) {
//         ElMessageBox.alert("登录状态已失效，请重新登陆", "提示", {
//           confirmButtonText: "确定",
//           callback: (action: Action) => {
//             router.push("/");
//           },
//         });
//       }
//     })
//     .catch((error: any) => {
//       uploading.value = false;
//       message.error("上传失败, 请重试");
//     });
// };

const showDrawer = ref(false);

const onClose = () => {
  showDrawer.value = false;
};
</script>

<style scoped>
.upload-button {
  width: 180px;
}

.private-algorithm-button {
  background-color: #ffffff;
  color: #333333;
  font-size: 16px;
  width: 100%;
  height: 100%;
  margin: 0;
  border-radius: 0;
  /*font-weight: 600;*/
  /*border: 1px solid #333333;*/
}
</style>
