datasetManagement.vue<template>
  <!-- <a-button @click="openCodeEditPanel">模型源码</a-button> -->
  <!-- <a-modal v-model:open="codeEditDialogVisible" title="模型源码编辑" :footer="null"> -->
    <div class="panel-container">
      <!-- 模块选择器 -->
      <div class="controls">
        <!-- <label for="module-selector">选择模块:</label> -->
        <a-space>
            <a-select v-model:value="selectedModule" @change="loadModuleCode" style="width: 200px">
                <a-select-option v-for="module in moduleCanEditCodeForTraining":value="module.value">{{ module.label }}</a-select-option>
            </a-select>
            <!-- <button @click="openDefaultFile">打开默认Python文件</button> -->
            <a-button @click="exportCode">导出代码</a-button>
            <!-- <input type="file" @change="importCode"> -->
        </a-space>
        
      </div>
      <!-- 编辑器容器 -->
      <div ref="editorContainer" class="editor"></div>
    </div>
  <!-- </a-modal> -->
</template>

<script>
import { ref, onMounted, watch } from 'vue';
import * as monaco from 'monaco-editor';

export default {
  props: {
    moduleWithCode: {
      type: Array,
      required: true
    },
    // pythonFilePaths: {
    //   type: Object,
    //   required: true
    // }
    canOpenCodeEditor: {
      type: Boolean,
      required: true
    }
  },
  setup(props) {
    const editorContainer = ref();
    let editor = null;
    const codeEditDialogVisible = ref(false);
    const selectedModule = ref('LSTM-故障诊断');

    onMounted(() => {
      editor = monaco.editor.create(editorContainer.value, {
        theme: "vs-white", // 主题
        value: "", // 默认显示的值
        acceptSuggestionOnCommitCharacter: false, // 接受关于提交字符的建议
        acceptSuggestionOnEnter: 'off', // 接受输入建议 "on" | "off" | "smart" 
        language: "python",
        folding: true, // 是否折叠
        foldingHighlight: true, // 折叠等高线
        foldingStrategy: "indentation", // 折叠方式  auto | indentation
        showFoldingControls: "always", // 是否一直显示折叠 always | mouseover
        disableLayerHinting: true, // 等宽优化
        emptySelectionClipboard: false, // 空选择剪切板
        selectionClipboard: false, // 选择剪切板
        automaticLayout: true, // 自动布局
        codeLens: false, // 代码镜头
        scrollBeyondLastLine: false, // 滚动完最后一行后再滚动一屏幕
        colorDecorators: true, // 颜色装饰器
        accessibilitySupport: "off", // 辅助功能支持  "auto" | "off" | "on"
        lineNumbers: "on", // 行号 取值： "on" | "off" | "relative" | "interval" | function
        lineNumbersMinChars: 5, // 行号最小字符   number
        enableSplitViewResizing: false,
        readOnly: false, //是否只读  取值 true | false
      });

      fetch('src/assets/exampleCode/train_lstm.py')
      .then(response => response.text())
      .then(data => {
        editor.setValue(data);
      })
      .catch(error => {
        console.error('无法打开文件:', error);
      });
    });

    const moduleCanEditCodeForTraining = [
        {
            label: '随机森林-故障诊断',
            value: 'faultDiagnosis-RandomForest'
        },
        {
            label: '支持向量机-故障诊断',
            value: 'faultDiagnosis-SVM'
        },
        {
            label: 'LSTM-故障诊断',
            value: 'faultDiagnosis-LSTM'
        },
        {
            label: 'GRU-故障诊断',
            value: 'faultDiagnosis-GRU'
        },
        {
            label: 'ulcnn-故障诊断',
            value: 'faultDiagnosis-ULCNN'
        },
        {
            label: 'simmodel-故障诊断',
            value: 'faultDiagnosis-SIMmodel'
        },
        {
            label: 'fdmssw-故障诊断',
            value: 'faultDiagnosis-fdmssw'
        },
        
    ]

    const pythonFilePaths = {
        'faultDiagnosis-RandomForest': 'src/assets/exampleCode/randomForestTrain.py',
        'faultDiagnosis-SVM': 'src/assets/exampleCode/svcTrain.py',
        'faultDiagnosis-LSTM': 'src/assets/exampleCode/train_lstm.py',
        'faultDiagnosis-GRU': 'src/assets/exampleCode/train_gru.py',
        'faultDiagnosis-ULCNN': 'src/assets/exampleCode/train_ulcnn.py',
        'faultDiagnosis-SIMmodel': 'src/assets/exampleCode/train_simmodel.py',
        'faultDiagnosis-fdmssw': 'src/assets/exampleCode/train_fdmssw.py',
        'healthEvaluation': 'src/assets/exampleCode/My-HE-Algorithm-1.py'
    }

    const loadModuleCode = () => {
      const filePath = pythonFilePaths[selectedModule.value];
      if (filePath) {
        fetch(filePath)
          .then(response => response.text())
          .then(data => {
            editor.setValue(data);
          })
          .catch(error => {
            console.error('无法打开文件:', error);
          });
      }
    };

    const openDefaultFile = () => {
      // 假设默认文件路径为 'path/to/default_file.py'
      fetch('src/assets/exampleCode/My-FD-Algorithm-1.py')
        .then(response => response.text())
        .then(data => {
          editor.setValue(data);
        })
        .catch(error => {
          console.error('无法打开文件:', error);
        });
    };

    const importCode = (event) => {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          editor.setValue(e.target.result);
        };
        reader.readAsText(file);
      }
    };

    const openCodeEditPanel = () => {
      codeEditDialogVisible.value = true;
    };

    const exportCode = () => {
      const content = editor.getValue();
      const blob = new Blob([content], { type: 'text/plain' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${selectedModule.value || 'modified_code'}.py`;
      a.click();
      window.URL.revokeObjectURL(url);
    };

    return {
      editorContainer,
      codeEditDialogVisible,
      selectedModule,
      loadModuleCode,
      openDefaultFile,
      importCode,
      openCodeEditPanel,
      exportCode,
      moduleCanEditCodeForTraining,
      pythonFilePaths
    };
  }
};
</script>

<style scoped>
.panel-container {
 
  width: 100%;
  max-height: 75vh;
}

.controls {
  margin-bottom: 20px;
}

.editor {
  width: 95%;
  height: 600px;
}
</style>