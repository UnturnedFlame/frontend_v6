<style lang="scss">
//vue flow 建模区域start
@import "vueflow/main.css";
//vue flow 建模区域end
</style>
<template>
  <!--
  更新页面 --v6.1
  版本  2024-12-25
  -->
  <div style="height: 100vh;overflow-x: hidden; font-family: 'Microsoft YaHei'">
    <el-container class="fullscreen_container">
      <!-- 头部栏目 -->
      <el-header class="header" style="z-index: 2;">
        <!-- 左侧的 Logo 区域 -->
        <div class="logo">
          <img src="../assets/system-logo.png" alt="Logo"/>
        </div>

        <!-- 中间的标题 -->
        <div class="title">
          <h1>轨道车辆智能运维通用算法和工具软件</h1>
        </div>

        <!-- 右侧的用户操作区 -->
        <div class="user-actions">
          <!-- 欢迎信息 -->
          <span class="welcome-message">{{
              username === '用户名未设置' ? '用户名未设置' : ('欢迎' + username + '！')
            }}</span>

          <!-- 帮助 -->
          <div class="clickable action-item">
            <el-dropdown :trigger="['click']" class="clickable" placement="bottom-end">
              <div style="display: flex; align-items: center; justify-content: center;">
                <i style="margin: 5px;" class="fa-regular fa-circle-question action-icon"></i>
                <a @click.prevent>
                  <span class="action-text" style="white-space: nowrap;overflow: hidden;">帮助</span>
                </a>
              </div>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="operationHelpDialogVisible=true">操作指南</el-dropdown-item>
                  <el-dropdown-item @click="userHelpDialogVisible=true">使用教程</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>

          <!-- 退出 -->
          <div @click="logout" class="clickable action-item">
            <i style="margin: 5px;" class="fa-solid fa-right-from-bracket action-icon"></i>
            <span class="action-text" style="white-space: nowrap;overflow: hidden;">退出</span>
          </div>

          <!-- 全屏 -->
          <div @click="toggleFullscreen()" class="clickable action-item" style="margin-right: 0;">
            <i v-if="!isFullScreen" style="margin: 5px;" class="fa-solid fa-expand action-icon"></i>
            <i v-else style="margin: 5px;" class="fa-solid fa-compress action-icon"></i>
            <span class="action-text" style="white-space: nowrap;overflow: hidden;">全屏</span>
          </div>
        </div>

        <!-- 操作指南 -->
        <el-dialog v-model="operationHelpDialogVisible" title="操作指南" width="810" draggable
                   :close-on-click-modal="false" :center="false">
          <div style="text-align: left;">
            <el-scrollbar height="500px">
              <h1>1、选择算法</h1>
              <h3>从算法选择区中将所选择算法模块拖拽至可视化建模区并调整位置</h3>
              <img src="../assets/step_1_drag.gif" alt="" style="width: 700px; height: auto">
              <h1>2、调整参数</h1>
              <h3>鼠标右击可视化建模区中的算法模块，在弹出的下拉框中更改算法的参数</h3>
              <img src="../assets/step_2_setting.gif" alt="" style="width: 700px; height: auto">
              <h1>3、建立流程</h1>
              <h3>鼠标移至作为所建立流程的起点的算法模块上的红色附着点，点击并拖拽至所建立流程的目标算法模块</h3>
              <img src="../assets/step_3_modeling.gif" alt="" style="width: 700px; height: auto">
              <h1>4、检查模型及修改模型</h1>
              <h3>在确保所有模块都已经建立流程后，点击完成建模，然后点击检查模型对所建立的模型进行检查，</h3>
              <h3>如果模型中存在错误，点击修改模型并根据提示对模型进行修改，然后依次点击完成建模和模型检查，</h3>
              <h3>通过模型检查后即可以保存模型，并进行后续操作。</h3>
              <img src="../assets/step_4_modelCheck.gif" alt="" style="width: 750px; height: auto">
            </el-scrollbar>
          </div>
        </el-dialog>

        <!-- 使用教程 -->
        <el-dialog v-model="userHelpDialogVisible" title="使用教程" width="810" draggable :close-on-click-modal="false"
                   :center="false">
          <div style="text-align: left;">
            <el-scrollbar height="500px" ref="userHelpDialogScrollbar">
              <h2>常见问题</h2>

              <div id="howToUseThisApp">
                <h2>1、如何使用本软件？</h2>
                <h3>本软件分为五个部分：①算法选择区、②数据加载区、③可视化建模区、④结果可视化区、⑤加载模型区。</h3>
                <img src="../assets/system-outline.png" alt="" style="width: 700px; height: auto">
                <h3>①<span style="color: red;">数据加载区</span>用于上传数据文件，查看用户的历史文件以及加载数据文件。
                </h3>
                <h3>②<span style="color: red;">算法选择区</span>中包含本系统支持的算法模块，可以选择其中的算法模块并拖入到可视化建模区进行建模。
                </h3>
                <h3>③<span style="color: red;">可视化建模区</span>是进行建模的区域，其中包含所有已经建立流程的算法模块，可以拖拽模块进行位置调整，也可以右击模块进行参数调整。
                </h3>
                <h3>④<span style="color: red;">结果可视化区</span>用于查看模型运行结果，包括模型运行结果图、模型运行结果表格。
                </h3>
                <h3>⑤<span style="color: red;">加载模型区</span>用于查看用户曾经保存的历史模型，和加载已保存的模型。</h3>
              </div>

              <div>
                <h2>2、如何在算法选择区中选择对应算法？</h2>
                <h3>在算法选择区中，每个模块都有三级展开结构，</h3>
                <img src="../assets/algorithms-unfold.png" alt="" style="width: 300px; height: auto">
                <h3>点击对应模块展开到最后一级，这时再点击对应算法会在结果可视化区中呈现该算法的介绍。</h3>
                <img src="../assets/algorithm-introduction.png" alt="" style="width: 700px; height: auto">
                <h3>通过拖动的方式可以将指定的算法模块拖入可视化建模区。并可以通过点击右键调整算法参数。</h3>
                <img src="../assets/set-params.png" alt="" style="width: 700px; height: auto">

              </div>

              <div>
                <h2>3、如何建立模型并保存？</h2>
                <h3>
                  在算法选择区中选择对应算法拖入到可视化建模区后，通过点击可视化建模区中算法模块上右侧的红色附着点，可以拉取一条连线并可连接到另一个算法模块上，以此来表示模型的运行顺序。</h3>
                <img src="../assets/line.gif" alt="" style="width: 700px; height: auto">
                <h3>在建立好模型后，点击完成建模，此时可以点击检查模型进行模型检查，具体操作步骤如下。</h3>
                <h3>第一步，点击完成建模</h3>
                <img src="../assets/modeling-finish-1.png" alt="" style="width: 700px; height: auto">
                <h3>第二步，点击检查模型。如果模型中存在错误，会呈现错误提示。</h3>
                <img src="../assets/modeling-finish-2.png" alt="" style="width: 700px; height: auto">
                <img src="../assets/check-model-tip.png" alt="" style="width: 700px; height: auto">

                <h3>第三步，如果模型中存在错误，点击修改模型并根据提示对模型进行修改，</h3>
                <img src="../assets/rectify-model-1.png" alt="" style="width: 700px; height: auto">
                <h3>
                  点击修改模型，此时提示正在修改模型，标红的连线表示该处存在逻辑错误，可以点击模块右上方红色的删除按钮删除报错模块，</h3>
                <img src="../assets/rectify-model-2.png" alt="" style="width: 700px; height: auto">
                <h3>删除报错模块后，正确建立模型流程，然后重复上述过程，直到通过模型检查，</h3>
                <img src="../assets/rectify-model-3.png" alt="" style="width: 700px; height: auto">

                <h3>第四步，完成上述流程后，点击保存模型进行模型的保存，</h3>
                <img src="../assets/save-model-1.png" alt="" style="width: 700px; height: auto">
                <h3>输入模型名称，点击确定，</h3>
                <img src="../assets/save-model-2.png" alt="" style="width: 700px; height: auto">

                <h3>其中建模时的模型检查遵循如下流程图中的规则，</h3>
                <img src="../assets/modeling-processing.png" alt="" style="width: 300px; height: auto">

              </div>

              <div>
                <h2>4、如何查看历史模型？</h2>
                <h3>在加载模型区中，点击用户历史模型，</h3>
                <img src="../assets/browser-saved-models-1.png" alt="" style="width: 700px; height: auto">
                <h3>
                  此时左侧弹窗中显示的就是用户保存过的历史模型，并且可以点击使用复现历史模型，点击删除历史模型，或是点击查看历史模型信息，</h3>
                <img src="../assets/browser-saved-models-2.png" alt="" style="width: 700px; height: auto">
                </img>
              </div>

              <div>
                <h2>5、如何上传文件到服务器？</h2>
                <h3>第一步，在数据加载区中，点击本地文件，</h3>
                <img src="../assets/upload-data-1.png" alt="" style="width: 700px; height: auto">

                <h3>
                  点击选择文件，选择本地文件，使其加载到文件列表中，每次只可以上传一个文件，并且可以点击文件列表中的删除图标要上传的文件，</h3>
                <img src="../assets/upload-data-3.png" alt="" style="width: 300px; height: auto">
                <h3>第二步，点击上传至服务器，根据提示输入文件名与文件描述，点击确定进行上传</h3>
                <img src="../assets/upload-data-2.png" alt="" style="width: 700px; height: auto">
              </div>

              <!-- <a href="javascript:void(0);" @click="scrollTo('howToUseThisApp')">1、如何使用本软件？</a>  -->

            </el-scrollbar>
          </div>
        </el-dialog>
      </el-header>
      <!-- 可视化建模主界面 -->
      <el-container style="flex-grow: 1;overflow-y: hidden;">
        <!-- 左侧菜单栏 -->
        <el-aside width="250"
                  class="el-aside-demo"
                  style="background: white;
                  overflow-y: auto;
                  overflow-x: hidden;
                  margin-right: 1px;
                  box-shadow: 3px 0 3px rgba(0, 0, 0, 0.2);
                  z-index: 2;
                  width: 250px;align-items: center;">
          <div style="width: 100%;">
            <!--      标题      -->
            <div class="aside-title"
                 style="font-size: 25px; color: #34374f;border: rgb(204,208,214) 1px solid;width: 100%;">
              <img src="../assets/algorithms-icon.svg"
                   style="width: 40px; height: auto; color: #34374f"/>
              <span v-if="userRole === 'superuser'">模型构建</span>
              <span v-if="userRole === 'user'">模型库</span>
            </div>
            <!--      菜单面板 accordion手风琴模式      -->
            <my-collapse
                v-model="activeNamesOfMenuPanel"
                :accordion="false"
                theme="light"
                @item-click="onItemClickOfMycollapse"
            >
              <my-collapse-item v-if="userRole === 'superuser'" name="1" :data="{name:'1'}" item-background="#ebeef4" style="border-bottom-width: 2px;">
                <!--      可以内容自定义，可以设置占满父div        -->
                <template #title>
                  <div style="padding: 10px;">
                    <span class="menu-item-first">基础组件</span>
                  </div>
                </template>
                <!--      可以不要图标，将下面删除即可          -->
                <template #arrow="{ isActive }">
                  <div style="align-items: center;padding-right: 10px;">
                    <i :class="['fa', isActive ? 'fa-caret-down' : 'fa-caret-right']"></i>
                  </div>
                </template>
                <!--      面板内容自定义          -->
                <div style="width: 100%;">
                  <my-collapse
                      v-model="activeNamesOfMenuPanel"
                      :accordion="true"
                      theme="light"
                      @item-click="onItemClickOfMycollapse"
                  >
                    <!--         数据源            -->
                    <my-collapse-item name="1-0" :data="{name:'1-0'}">
                      <template #title>
                        <div style="padding: 10px 0 10px 20px;">
                          <span style="font-family: 'Microsoft YaHei';font-size: 18px">数据源</span>
                        </div>
                      </template>
                      <template #arrow="{ isActive }">
                        <div style="align-items: center;padding-right: 10px;">
                          <i :class="['fa', isActive ? 'fa-caret-down' : 'fa-caret-right']"></i>
                        </div>
                      </template>
                      <div
                          style="width: 100%;display: flex;flex-wrap: wrap;gap: 0;padding: 0;background-color: #ffffff;flex-direction: column;">
                        <div :draggable="true"
                             style="width: 100%;"
                             class="menu-item-second"
                             @dragstart="onDragStart($event,'dataSource',dataSourceNode,'handleDragend','default')"
                             @click="showIntroduction('dataSource'.replace(/_multiple/g, ''))"
                        >
                          <DragModelItem
                              :text="'数据源组件'"
                              :tooltip_text="'拖拽数据源组件至可视化建模区'"
                              :custom-styles="{
                                 backgroundColor: '#ffffff',
                                 width: '250px',
                                 height: '40px',
                              }"
                              :content-style="{
                                 backgroundColor: '#ffffff',
                                 paddingLeft: '50px',
                                 paddingRight: '10px',
                                 fontSize: '18px'
                              }"
                          >
                            <template #icon>
                              <i class="fa-solid fa-database"></i>
                            </template>
                            <!-- <template #default>
                              <span> 数据源组件</span>
                            </template> -->
                            
                          </DragModelItem>
                        </div>
                      </div>
                    </my-collapse-item>
                    <!--         中间组件的一级目录             -->
                    <my-collapse-item v-for="(item,index1) in menuList2"
                                      :name="'1-'+(index1+1)"
                                      :data="{name: '1-'+(index1+1)}">
                      <template #title>
                        <div style="padding: 10px 0 10px 20px;">
                          <span style="font-size: 18px;">{{ item.label }}</span>
                        </div>
                      </template>
                      <template #arrow="{ isActive }">
                        <div style="align-items: center;padding-right: 10px;">
                          <i :class="['fa', isActive ? 'fa-caret-down' : 'fa-caret-right']"></i>
                        </div>
                      </template>
                      <div style="width: 100%;display: flex;flex-wrap: wrap;
                          gap: 0;padding: 0;background-color: #ffffff;">
                        <!--           中间组件的二级目录           -->
                        <my-collapse
                            v-model="activeNamesOfMenuPanel"
                            :accordion="true"
                            theme="light"
                            @item-click="onItemClickOfMycollapse"
                        >
                          <!--            v-if="menuDetailsSecond[item.label]"              -->
                          <my-collapse-item v-for="(option,index2) in item.options"
                                            :name="'1-'+(index1+1)+'-'+(index2)"
                                            :data="{name: '1-'+(index1+1)+'-'+(index2)}"
                                            @click="clickAtSecondMenu(option)"
                          >
                            <template #title>
                              <div style="padding: 10px 0 10px 30px;display: flex;align-items: center;">
                                <img style="height: 20px;width: 20px;" :src="setIconOfAlgorithms(option.label)"
                                     alt="none"/>
                                <span
                                  class="menu-item-second"
                                  style="margin-left: 8px;">
                                  {{option.label}}</span>
                              </div>
                            </template>
                            <template #arrow="{ isActive }">
                              <div style="align-items: center;padding-right: 10px;">
                                <i :class="['fa', isActive ? 'fa-caret-down' : 'fa-caret-right']"></i>
                              </div>
                            </template>
                            <div
                                style="width: 100%;display: flex;gap: 0;padding: 0;background-color: #ffffff;flex-direction: column;">
                              <!--              中间组件的三级图标 v-if="menuDetailsThird[option.label]"
                              @dragend="handleDragend($event, algorithm, option)"
                              -->
                              <div v-for="algorithm in Object.keys(option.parameters)"
                                   :draggable="true"
                                   style="width: 100%;"
                                   @dragstart="onDragStart($event,algorithm, option,'handleDragend','default')"
                                   @click="showIntroduction(algorithm.replace(/_multiple/g, ''))"
                              >
                                <!--                                :bgColor="'#fefefe'"-->
                                <DragModelItem
                                    :text="labelsForAlgorithms[algorithm]"
                                    :tooltip_text="labelsForAlgorithms[algorithm]"
                                    :custom-styles="{
                                      // backgroundColor: '#1a5be8',
                                      backgroundColor: '#ffffff',
                                      width: '250px',
                                      height: '40px',
                                    }"
                                    :content-style="{
                                      // backgroundColor: '#151414',
                                      backgroundColor: '#ffffff',
                                      paddingLeft: '40px',
                                      paddingRight: '10px',
                                    }"
                                >
                                  <template #icon>
                                    <!--                                    <i class="fa-solid fa-puzzle-piece" style="border: red solid 2px;"></i>-->
                                    <i class="fa-solid fa-puzzle-piece"></i>
                                  </template>
                                </DragModelItem>
                              </div>
                            </div>
                          </my-collapse-item>
                        </my-collapse>
                      </div>
                    </my-collapse-item>
                    <!--         增值组件           -->
                    <my-collapse-item name="1-0-0" :data="{name:'1-0-0'}">
                      <template #title>
                        <div style="padding: 10px 0 10px 20px;">
                          <span style="font-size: 18px;">增值组件</span>
                        </div>
                      </template>
                      <template #arrow="{ isActive }">
                        <div style="align-items: center;padding-right: 10px;">
                          <i :class="['fa', isActive ? 'fa-caret-down' : 'fa-caret-right']"></i>
                        </div>
                      </template>
                      <div
                          style="width: 100%;display: flex;flex-wrap: wrap;gap: 0;padding: 0;background-color: #ffffff;flex-direction: column;">
                        <div :draggable="true"
                             style="width: 100%;"
                             v-for="(dataSourceNode,index) in fetchedExtraAlgorithmList"
                             :index="index"
                             @dragstart="onDragStart($event,dataSourceNode.alias,dataSourceNode,'handleDragendAdd','default')">
                          <DragModelItem
                              :text="dataSourceNode.alias"
                              :tooltip_text="dataSourceNode.alias"
                              :custom-styles="{
                                 backgroundColor: '#ffffff',
                                 width: '250px',
                                 height: '40px',
                              }"
                              :content-style="{
                                 backgroundColor: '#ffffff',
                                 paddingLeft: '40px',
                                 paddingRight: '10px',
                              }"
                          >
                            <template #icon>
                              <i class="fa-solid fa-puzzle-piece"></i>
                            </template>
                          </DragModelItem>
                        </div>
                      </div>
                    </my-collapse-item>
                  </my-collapse>
                </div>
              </my-collapse-item>
              <my-collapse-item v-if="userRole === 'superuser'" name="2" :data="{name:'2'}" item-background="#ebeef4" style="border-bottom-width: 2px;">
                <template #title>
                  <div style="padding: 10px;">
                    <span style="font-size: 20px;">新增组件</span>
                  </div>
                </template>
                <template #arrow="{ isActive }">
                  <div style="align-items: center;padding-right: 10px;">
                    <i :class="['fa', isActive ? 'fa-caret-down' : 'fa-caret-right']"></i>
                  </div>
                </template>
                <div style="width: 100%;">
                  <!-- 上传增值服务组件，只对系统用户可见 -->
                  <!--            <el-divider style="height: 5px;background: #CDCFD0;margin-top: 16px;margin-bottom: 0;"/>-->
                  <div v-if="userRole === 'superuser'"
                       style="width: 100%;flex-direction: column;display: flex;">
                    <div
                        style="width: 100%;flex: 1;display: flex;
                        flex-direction: column;align-items: center;justify-content: center;
                        margin-right: 1px;"
                    >
                      <uploadPrivateAlgorithmFiless style="width: 100%;height: 100%;"
                                                    @addExtraModule="handleAddExtraModule"/>
                    </div>
                    <div
                        style="width: 100%;flex: 1;display: flex;
                        flex-direction: column;align-items: center;justify-content: center;
                        margin-right: 1px;"
                    >
                      <managePrivateAlgorithm style="width: 100%;height: 100%;"
                                              @deleteExtraModule="handleDeleteExtraModule"/>
                    </div>
                  </div>
                </div>
              </my-collapse-item>
              
              <my-collapse-item v-if="userRole === 'user'" name="4" :data="{name:'4'}" item-background="#ebeef4">
                
                  <!-- 搜索框 -->
                  <!-- <div style="
                       width: 100%;
                       display: flex;
                       flex-direction: column;">
                       <el-input
                          v-model="searchKeywordOfTree"
                          placeholder="请输入关键字查询"
                          style="width: 100%; margin-bottom: 5px;"
                      />
                    
                    <div style="flex: 1; /* 让树形结构占据剩余空间 */
                         overflow-x: auto; /* 如果树形结构宽度超出屏幕宽度，显示横向滚动条 */">
                      <div style="width: 100%;overflow-x: auto">
                        <div style="">
                          <el-tree
                              ref
                              ="treeRef"
                              :data="filteredDataOfTree"
                              style="width: 100%;max-width: 100%;"
                              node-key="id"
                              :expand-on-click-node="false"
                              :default-expand-all="isExpandAllOfTree"
                              :filter-node-method="filterNodeOfTree"
                              :accordion="false"
                          >
                            <template #default="{ node, data }">
                      <span class="custom-tree-node" style="">
                        <span class="node-label">{{ node.label }}</span>
                        <span class="node-actions">
                          <el-icon v-if="node.isLeaf" @click="nodeModelOfTree(node, data)" :style="{color:'#409eff'}">
                               <i class="fa-solid fa-hexagon-nodes"></i>
                          </el-icon>
                        </span>
                      </span>
                            </template>
                          </el-tree>
                        </div>
                      </div>
                      <el-dialog
                          v-model:visible="isEditDialogVisibleOfTree"
                          title="编辑节点"
                          :close-on-click-modal="false"
                          :before-close="handleCloseOfTree"
                      >
                        <el-input
                            v-model="editNodeLabelOfTree"
                            placeholder="请输入新的节点名称"
                            :autofocus="true"
                        />
                        <span slot="footer" class="dialog-footer">
                          <el-button @click="isEditDialogVisibleOfTree = false">取消</el-button>
                          <el-button type="primary" @click="saveEditOfTree">保存</el-button>
                        </span>
                      </el-dialog>
                    </div>
                  </div> -->
                  

                  <template #title>
                    <div style="padding: 10px;">
                      <span style="font-size: 20px;">模型结构树</span>
                    </div>
                  </template>
                  <template #arrow="{ isActive }">
                    <div style="align-items: center;padding-right: 10px;">
                      <i :class="['fa', isActive ? 'fa-caret-down' : 'fa-caret-right']"></i>
                    </div>
                  </template>
                  <div class="custom-tree-container" style="width: 100%;">
                    <ComponentTree :userRole="userRole" @loadModel="handleLoadModel"/>
                  </div>
              </my-collapse-item>
              <my-collapse-item name="5" :data="{name:'5'}" item-background="#ebeef4">
                <template #title>
                  <div style="width: 100%">
                    <datasetManagement/>
                  </div>
                </template>
              </my-collapse-item>

              <!-- 组件代码修改 -->
              <my-collapse-item v-if="userRole === 'superuser'" @click="openCodeEditPanel" name="6" :data="{name:'6'}" item-background="#ebeef4">
                <template #title>
                  <div style="padding: 10px;">
                    <span style="font-size: 20px; width: 100%" >组件代码</span>
                  </div>
                  <!-- 修改源码 -->
                 <div>
                   <a-modal v-model:open="codeEditDialogVisible" title="组件代码编辑" :footer="null" style="width: 60%">
                     <editCodeEmbedded :moduleWithCode="moduleWithCode" :canOpenCodeEditor="canOpenCodeEditor"/>
                   </a-modal>
                 </div>
                </template>
              </my-collapse-item>

              <!-- 模型管理 -->
              <my-collapse-item v-if="userRole === 'superuser'" name="7" :data="{name:'7'}" item-background="#ebeef4">
                <template #title>
                  <div style="padding: 10px;">
                    <span style="font-size: 20px;">模型库</span>
                  </div>
                </template>
                <template #arrow="{ isActive }">
                  <div style="align-items: center;padding-right: 10px;">
                    <i :class="['fa', isActive ? 'fa-caret-down' : 'fa-caret-right']"></i>
                  </div>
                </template>
                <div style="width: 100%;">
                  <!-- 上传增值服务组件，只对系统用户可见 -->
                  <!--            <el-divider style="height: 5px;background: #CDCFD0;margin-top: 16px;margin-bottom: 0;"/>-->
                  <div v-if="userRole === 'superuser'"
                       style="width: 100%;flex-direction: column;display: flex;">
                    <div
                        style="width: 100%;flex: 1;display: flex;
                        flex-direction: column;align-items: center;justify-content: center;
                        margin-right: 1px;"
                    >
                      <PublishModel style="width: 100%;height: 100%;" :userRole="userRole" @resetModel="handleResetModel" @loadModel="handleLoadModel"/>
                    </div>
              
                  </div>
                </div>
                
              
                
              </my-collapse-item>

              <!-- 终端用户模型结构树 -->
              <my-collapse-item v-if="userRole === 'superuser'" name="8" :data="{name:'8'}" item-background="#ebeef4">
                <template #title>
                  <div style="padding: 10px;">
                    <span style="font-size: 20px;">模型结构树</span>
                  </div>
                </template>
                <template #arrow="{ isActive }">
                  <div style="align-items: center;padding-right: 10px;">
                    <i :class="['fa', isActive ? 'fa-caret-down' : 'fa-caret-right']"></i>
                  </div>
                </template>
                <div class="custom-tree-container" style="width: 100%;">
                  <ComponentTree :userRole="userRole" ref="superComponentTree" @resetModel="handleResetModel" @loadModel="handleLoadModel"/>
                </div>
              </my-collapse-item>
            </my-collapse>
          </div>
        </el-aside>

        <!-- 可视化建模区以及结果可视化区 -->
        <el-main @dragover.prevent ref="efContainerRef" id="efContainer"
                 style="padding: 0;height: 100%;background: white">
          <div class="parent-containerOfElMain">
            <!-- 建模部分 -->
            <div class="modeling-areaOfElMain">
              <div style="width: 100%;height: 100%;" @drop="onDrop">
                <VueFlow
                  v-model:nodes="modeling_nodeList"
                  :edges="modeling_edgesList"
                  :class="{ dark }"
                  class="basic-flow"
                  :default-viewport="{ zoom: 1 }"
                  :min-zoom="0.5"
                  :max-zoom="4"
                  @dragover="onDragOver"
                  @dragleave="onDragLeave"
                  @node-click="handleNodeClick"
                  @edges-change="change => handleEdgesChange(change)"
                >
                  <div id="statusIndicator" class="status-indicator">未建立模型</div>
                  <!-- 背景 -->
                  <DragDropzoneBackground
                      :style="{backgroundColor: isDragOver ? '#e7f3ff' : 'transparent',transition: 'background-color 0.2s ease',}"
                  >
                    <!-- <p v-if="isDragOver">拖入到此</p> -->
                  </DragDropzoneBackground>
                  <!-- 基础操作栏 -->
                  <Controls @interaction-change="onInteractionChangeOfControls" position="top-left" >
                    <ControlButton title="重置" @click="modeling_resetTransform" class="menu-item-second"> 
                      <Icon name="reset"/>
                    </ControlButton>

                    <ControlButton title="打乱" @click="modeling_updatePos">
                      <Icon name="update"/>
                    </ControlButton>

                    <ControlButton title="背景" @click="modeling_toggleDarkMode">
                      <Icon v-if="dark" name="sun"/>
                      <Icon v-else name="moon"/>
                    </ControlButton>

                    <ControlButton title="垂直布局" @click="layoutGraph('LR')">
                      <i :style="dark ? 'color: #ffffff' : 'color: #000000'" class="fa-solid fa-arrows-up-down"></i>
                    </ControlButton>

                    <ControlButton title="水平布局" @click="layoutGraph('TB')">
                      <i :style="dark ? 'color: #ffffff' : 'color: #000000'" class="fa-solid fa-arrows-left-right"></i>
                    </ControlButton>

                    <ControlButton title="打印边、节点数据（object）" @click="modeling_test_logToObject">
                      <Icon name="log"/>
                    </ControlButton>

                    <ControlButton title="测试保存模型到localStorage" @click="modeling_test_onSave">
                      <Icon name="log"/>
                    </ControlButton>

                    <ControlButton title="测试恢复模型从localStorage" @click="modeling_test_onRestore">
                      <Icon name="log"/>
                    </ControlButton>
                  </Controls>
                  <!-- 功能操作栏 -->
                  <Controls position="top-right" :show-zoom="false" :show-fit-view="false" :show-interactive="false"
                            class="menu-item-second"
                            style="display: flex;flex-direction: row;right: 300px;">
                    <ControlButton
                        @click="outputConfig"
                        class="control-operator-btn-default-css"
                        :disabled="disabledStateOfControlBtn.clearModelOfViewFlowBtn"
                        :style="{color: dark ? '#ffffff' : '#000000'}"
                        title="下载报告">
                              <i class="fa-solid fa-download"></i>
                      <span class="menu-item-second" >报告</span>
                    </ControlButton>
                    <ControlButton
                        @click="clearModelOfViewFlow"
                        class="control-operator-btn-default-css"
                        :disabled="disabledStateOfControlBtn.clearModelOfViewFlowBtn"
                        :style="{color: dark ? '#ffffff' : '#000000'}"
                        title="清空模型">
                      <i class="fa-solid fa-broom"></i>
                      <span class="menu-item-second" >清空</span>
                    </ControlButton>
                    <ControlButton
                        v-if="userRole === 'superuser'"
                        @click="checkModelOfViewFlow"
                        class="control-operator-btn-default-css"
                        :disabled="disabledStateOfControlBtn.checkModelOfViewFlowBtn"
                        :style="{color: dark ? '#ffffff' : '#000000'}"
                        title="检查模型">
                      <i class="fa-solid fa-magnifying-glass"></i>
                      <span class="menu-item-second" >检查</span>
                    </ControlButton>
                    <ControlButton
                        v-if="userRole === 'superuser'"
                        @click="saveModelOfViewFlow"
                        class="control-operator-btn-default-css"
                        :disabled="disabledStateOfControlBtn.saveModelOfViewFlowBtn"
                        :style="{color: dark ? '#ffffff' : '#000000'}"
                        title="保存模型">
                      <i class="fa-solid fa-floppy-disk"></i>
                      <span class="menu-item-second" >保存</span>
                    </ControlButton>
                    <ControlButton
                        @click="runModelOfViewFlow"
                        class="control-operator-btn-default-css"
                        :disabled="disabledStateOfControlBtn.runModelOfViewFlowBtn"
                        :style="{color: dark ? '#ffffff' : '#000000'}"
                        title="运行模型">
                      <i class="fa-solid fa-power-off"></i>
                      <span class="menu-item-second" >运行</span>
                    </ControlButton>
                    <ControlButton
                        @click="openConfigPanelOfModelNode"
                        class="control-operator-btn-default-css"
                        :disabled="disabledStateOfControlBtn.configPanelOfModelNodeBtn"
                        :style="{color: dark ? '#ffffff' : '#000000'}"
                        title="模型配置">
                      <i class="fa-solid fa-gear"></i>
                      <span class="menu-item-second" >配置</span>
                    </ControlButton>
                  </Controls>
                  <!-- 自定义节点 -->
                  <template #node-menu="props">
                    <!-- <ModelingCustomNode :id="props.id" :data="props.data"/> -->
                    <ModelingCustomNode :id="props.id" :data="props.data" @showResults="handleNodeClick"/>
                  </template>
                  <!-- 自定义边 -->
                  <template #edge-button="buttonEdgeProps">
                    <ModelingCustomEdge
                        :id="buttonEdgeProps.id"
                        :source-x="buttonEdgeProps.sourceX"
                        :source-y="buttonEdgeProps.sourceY"
                        :target-x="buttonEdgeProps.targetX"
                        :target-y="buttonEdgeProps.targetY"
                        :source-position="buttonEdgeProps.sourcePosition"
                        :target-position="buttonEdgeProps.targetPosition"
                        :marker-end="buttonEdgeProps.markerEnd"
                        :style="buttonEdgeProps.style"
                        :remove-btn-disabled="removeBtnDisabled"
                    />
                  </template>
                </VueFlow>
              </div>
            </div>

            <!--配置部分-->
            <div :class="['configPanelOfModelNode', { hidden: isHiddenConfigPanelOfNode }]">
              <div class="closeConfigPanelBtnOfModelNode">
                <button
                    class="icon-buttonOfElMain"
                    @click="closeConfigPanelOfModelNode"
                >
                  <i class="fa-solid fa-xmark"></i>
                </button>
              </div>
              <div class="configAreaPanelOfModelNode">
                <my-collapse
                    v-model="activeNamesOfConfigPanelOfModelNode"
                    :accordion="true"
                    theme="light"
                    style="background-color: #3c93f8"
                    @item-click="onItemClickOfConfigPanelOfModelNode"
                >
                  <!-- 数据源配置 -->
                  <my-collapse-item v-if="containsMenuSettings.includes('4')" name="4-" :data="{name:'4-'}"
                                    item-background="#ebeef4">
                    <template #title>
                      <div style="padding: 6px;">
                        <span style="font-size: 18px;">数据源配置</span>
                      </div>
                    </template>
                    <template #arrow="{ isActive }">
                      <div style="align-items: center;padding-right: 10px;">
                        <i :class="['fa-solid', isActive ? 'fa-angle-down' : 'fa-angle-right']"></i>
                      </div>
                    </template>
                    <div class="" style="width: 100%;background-color: white;">
                      <div style="font-size: 18px">加载数据集</div>
                      <a-button
                              type="default"
                              style="margin-top: 25px; margin-left: 0px; width: 160px; font-size: 16px;  background-color: #2082F9; color: white"
                              @click="openDatasetLoadingPanel"
                              :icon="h(FolderOutlined)">
                              从数据库加载
                      </a-button>
                      <!-- 分割线 -->
                      <!-- <div style="width: 2px; height: 136px; background-color: #808080; position: absolute; right: 185px; bottom: 0px; border-radius: 1px;"></div> -->
                      <!-- 显示已加载的数据名称 -->
                      
                      <!-- <div style="font-size: 18px; font-weight: 600">已加载数据</div> -->
                      <div class="highlight"
                          :style="{ color: getColor(usingDatafile), position: 'relative', 'margin-top': '30px', 'max-width': '300px', 'word-wrap': 'break-word' }"
                          :title="usingDatafile">
                        {{usingDatafile!='无' ? '已加载数据：' + usingDatafile : '当前未加载数据'  }}
                      </div>
                      
                    </div>
                    <el-dialog v-model="datasetManagementDialog" width="1000px">
                      <template #header>
                        <div>
                          <p style="font-weight: bold; font-size: 20px">数据加载</p>
                        </div>
                      </template>
                      
                      <div style="display: flex; flex-direction: column;">
                        <h2 style="margin-bottom: 25px; color: #253b45; text-align: left; font-size: 25px;">用户数据文件</h2>
                        <div style="display: flex; flex-direction: row; width: 30%">
     
                          <el-input v-model="searchDataKeyword" placeholder="输入文件名" style="width: 50%">
                          </el-input>
                          
                          <el-button type="primary" style="width: 20%; margin-left: 10px" @click="searchDataset">搜索</el-button>
                        </div>
                        <el-table :data="fetchedDataFiles" height="500" stripe width="100%">
                          <el-table-column property="owner" label="文件上传者" show-overflow-tooltip/>
                          <el-table-column property="dataset_name" label="文件名称" show-overflow-tooltip/>
                          <el-table-column property="description" label="文件描述" show-overflow-tooltip/>
                          <el-table-column label="操作">
                            <template #default="scope">
                              <el-button
                                  size="small"
                                  type="primary"
                                  style="width: 50px"
                                  @click="useDataset(scope.row)"
                                  :loading="loadingData"
                              >
                                {{ loadingData? '加载中' : '加载' }}
                              </el-button>
                              
                              <el-popconfirm title="你确定要删除该数据文件吗"
                                            @confirm="deleteDatasetConfirm(scope.$index, scope.row)">
                                <template #reference>
                        
                                </template>
                                <template #actions="{ confirm, cancel }">
                                  <el-row>
                                    <el-col :span="12">
                                      <el-button size="small" @click="cancel">取消</el-button>
                                    </el-col>
                                    <el-col :span="12">
                                      <el-button
                                          type="primary"
                                          size="small"
                                          @click="confirm"
                                      >
                                        确定
                                      </el-button>
                                    </el-col>
                                  </el-row>
                                </template>
                              </el-popconfirm>

                              <el-button
                                  size="small"
                                  type="success"
                                  style="width: 50px"
                                  @click="browseDataset(scope.row)"
                              >
                                查看
                              </el-button>
                            </template>
                          </el-table-column>
                        </el-table>
                      </div>
                    </el-dialog>
                  </my-collapse-item>
                  <!-- 特征提取参数配置 -->
                  <my-collapse-item v-if="containsMenuSettings.includes('1.2')" name="1.2-" :data="{name:'1.2-'}"
                                    item-background="#ebeef4">
                    <template #title>
                      <div style="padding: 6px;">
                        <span style="font-size: 16px; font-family: 'Microsoft YaHei';">特征提取参数配置</span>
                      </div>
                    </template>
                    <template #arrow="{ isActive }">
                      <div style="align-items: center;padding-right: 10px;">
                        <i :class="['fa-solid', isActive ? 'fa-angle-down' : 'fa-angle-right']"></i>
                      </div>
                    </template>
                    <div class="" style="width: 100%;background-color: white;">
                      <div style="width: 100%;display: flex;flex-direction: column; font-family: 'Microsoft YaHei';">
                        <div style="flex: 1;padding: 10px;width: 100%;">
                          <el-text style="font-size: 15px; ">选择特征<span
                              style="font-size: 12px;">(共{{
                              Object.keys(modeling_nodeList[parameter_dict[transfer['特征提取']]].nodeInfo.parameters[transfer['特征提取']]).length
                            }}个可选特征)</span></el-text>
                        </div>
                        <div style="flex: 1;width: 100%;padding-bottom: 10px;">
                          <!-- <el-select v-model="features" multiple collapse-tags collapse-tags-tooltip
                                     :max-collapse-tags="5" popper-class="select"
                                     placeholder="选择需要提取的特征" :teleported="false" style="width: 90%;">
                            <el-option v-for="(value, key) in modeling_nodeList[parameter_dict[transfer['特征提取']]].nodeInfo.parameters[transfer['特征提取']]" :label="key"
                                       :value="key" style="width: 200px; background-color: white;"/>
                          </el-select>
                          <a-select>
                            <a-select-option></a-select-option>
                          </a-select> -->
                          <a-select v-model:value="features" mode="multiple" :max-tag-count="5" placeholder="选择需要提取的特征" style="width: 90%;">
                            <a-select-option
                              v-for="(value, key) in modeling_nodeList[parameter_dict[transfer['特征提取']]].nodeInfo.parameters[transfer['特征提取']]"
                              :key="key"
                              :value="key"
                              style="width: 200px; background-color: white;"
                            >
                              {{ key }}
                            </a-select-option>
                          </a-select>
<!--                          <a-select-->
<!--                              v-model:value="value"-->
<!--                              mode="multiple"-->
<!--                              style="width: 100%"-->
<!--                              placeholder="Please select"-->
<!--                              :options="modeling_nodeList[parameter_dict[transfer['特征提取']]].nodeInfo.parameters[transfer['特征提取']]"-->
<!--                          ></a-select>-->
                        </div>
                      </div>
                    </div>
                  </my-collapse-item>
                  <!-- 特征选择参数配置-->
                  <!-- 选择特征选择的规则以及设定规则的阈值 -->
                  <my-collapse-item
                      v-if="containsMenuSettings.includes('1.3') && item.use_algorithm !== 'extra_feature_selection'"
                      name="1.3" :data="{name:'1.3'}"
                      item-background="#ebeef4">
                    <template #title>
                      <div style="padding: 6px;">
                        <span style="font-size: 16px; font-family: 'Microsoft YaHei';">特征选择参数配置</span>
                      </div>
                    </template>
                    <template #arrow="{ isActive }">
                      <div style="align-items: center;padding-right: 10px;">
                        <i :class="['fa-solid', isActive ? 'fa-angle-down' : 'fa-angle-right']"></i>
                      </div>
                    </template>
                    <div class="" style="width: 100%;">
                      <div style="background-color: white; display: flex; flex-direction: column; padding: 20px">
                        <el-radio-group v-model="modeling_nodeList[parameter_dict[transfer['特征选择']]].nodeInfo.parameters[transfer['特征选择']]['rule']">
                          <el-radio :value="1" size="large">规则一</el-radio>
                          <el-radio :value="2" size="large">规则二</el-radio>
                        </el-radio-group>
                        <!-- 特征选择规则一 -->
                        <div v-if="modeling_nodeList[parameter_dict[transfer['特征选择']]].nodeInfo.parameters[transfer['特征选择']]['rule'] == 1">
                          <div style="margin-top: 5px; margin-bottom: 15px;">
                            设定阈值后，将选择重要性系数大于该阈值的特征
                          </div>
                          <el-form>
                            <el-form-item label="阈值">
                              <el-input-number v-model="modeling_nodeList[parameter_dict[transfer['特征选择']]].nodeInfo.parameters[transfer['特征选择']]['threshold1']"
                                               :precision="2" :step="0.05" :max="1" :min="0"/>
                            </el-form-item>
                          </el-form>
                        </div>
                        <!-- 特征选择规则二 -->
                        <div v-if="modeling_nodeList[parameter_dict[transfer['特征选择']]].nodeInfo.parameters[transfer['特征选择']]['rule'] == 2">
                          <div style="margin-top: 5px; margin-bottom: 15px;">
                            设定阈值后，将根据特征的重要性，由高到低地选择特征，直到所选特征的重要性的总和占所有特征的重要性比例不小于该阈值，其中所有特征的重要性占比为1
                          </div>
                          <el-form>
                            <el-form-item label="阈值">
                              <el-input-number v-model="modeling_nodeList[parameter_dict[transfer['特征选择']]].nodeInfo.parameters[transfer['特征选择']]['threshold2']"
                                               :precision="2" :step="0.05" :max="1" :min="0"/>
                            </el-form-item>
                          </el-form>
                        </div>
                      </div>
                    </div>
                  </my-collapse-item>
                  <!-- 无量纲化参数设置 -->
                  <my-collapse-item v-if="containsMenuSettings.includes('1.5')" name="1.5-" :data="{name:'1.5-'}"
                                    item-background="#ebeef4">
                    <template #title>
                      <div style="padding: 6px;">
                        <span style="font-size: 16px;font-family: 'Microsoft YaHei';">无量纲化参数设置</span>
                      </div>
                    </template>
                    <template #arrow="{ isActive }">
                      <div style="align-items: center;padding-right: 10px;">
                        <i :class="['fa-solid', isActive ? 'fa-angle-down' : 'fa-angle-right']"></i>
                      </div>
                    </template>
                    <div class="" style="width: 100%;background-color: white;padding-top: 10px;">
                      <div>是否使用模型训练时的标准化方法?</div>
                      <el-radio-group v-model="modeling_nodeList[parameter_dict[transfer['无量纲化']]].nodeInfo.parameters[transfer['无量纲化']]['useLog']">
                        <el-radio :value="true" size="large">是</el-radio>
                        <el-radio :value="false" size="large">否</el-radio>
                      </el-radio-group>
                    </div>
                  </my-collapse-item>
                  <!--小波变换参数配置-->
                  <my-collapse-item v-if="containsMenuSettings.includes('1.4')" name="1.4-" :data="{name:'1.4-'}"
                                    item-background="#ebeef4">
                    <template #title>
                      <div style="padding: 6px;">
                        <span style="font-size: 16px;font-family: 'Microsoft YaHei';">小波变换参数配置</span>
                      </div>
                    </template>
                    <template #arrow="{ isActive }">
                      <div style="align-items: center;padding-right: 10px;">
                        <i :class="['fa-solid', isActive ? 'fa-angle-down' : 'fa-angle-right']"></i>
                      </div>
                    </template>
                    <div class="" style="width: 100%;">
                      <div style="background-color: white; display: flex; flex-direction: column; padding-top: 20px;">
                        <el-row
                            v-for="(value, key) in modeling_nodeList[parameter_dict[transfer['小波变换']]].nodeInfo.parameters[transfer['小波变换']]"
                            :key="key" style="margin-bottom: 20px">
                          <el-col :span="10" style="align-content: center;"><span
                              style="margin-left: 10px; font-size: 15px;">{{ labelsForParams[key] }}：</span></el-col>
                          <el-col :span="12">
                            <!-- <el-select v-model="modeling_nodeList[parameter_dict[transfer['小波变换']]].nodeInfo.parameters[transfer['小波变换']][key]" collapse-tags
                                       collapse-tags-tooltip :teleported="false" placeholder="请选择参数">
                              <el-option
                                  v-for="item in recommendParams[key]"
                                  :key="item.value"
                                  :label="item.label"
                                  :value="item.value"
                                  style="width: 200px; height: auto; background-color: white;"
                              />
                            </el-select> -->
                            <a-select v-model:value="modeling_nodeList[parameter_dict[transfer['小波变换']]].nodeInfo.parameters[transfer['小波变换']][key]" placeholder="请选择参数" style="width: 90%;">
                              <a-select-option
                                v-for="item in recommendParams[key]"
                                :key="item.value"
                                :value="item.value"
                                style="background-color: white;"
                              >
                                {{ item.label }}
                              </a-select-option>
                            </a-select>
                          </el-col>
                        </el-row>
                      </div>
                    </div>
                  </my-collapse-item>
                  <!-- 其他常规配置 -->
                  <div
                      v-if="!containsMenuSettings.includes('4')
                      && !containsMenuSettings.includes('1.2')
                      && !containsMenuSettings.includes('1.3')
                      && !containsMenuSettings.includes('1.4')
                      && !containsMenuSettings.includes('1.5')"
                      style="background-color: white; font-family: 'Microsoft YaHei'; display: flex; flex-direction: column; padding-top: 30px;height: 100%;">
                    暂无可调参数
                  </div>
                </my-collapse>
              </div>
            </div>

            <!-- 运行结果部分 -->
            <transition name="slide">
              <div
                  v-show="isResultVisibleOfElMain"
                  v-if="isResultVisibleOfElMain"
                  class="result-areaOfElMain"
                  :style="{ height: resultHeightOfElMain + 'px' }"
              >
                <!-- 运行结果头部，可拖动 -->
                <div class="result-headerOfElMain" @mousedown="initDragOfElMain" @touchstart="initDragTouchOfElMain">
<!--                                    <span>运行结果部分</span>-->
                  <div class="buttonsOfElMain">
                    <button
                        class="icon-buttonOfElMain"
                        @click="closeResultOfElMain"
                        aria-label="隐藏结果"
                        @keydown.enter.prevent="closeResultOfElMain"
                        @keydown.space.prevent="closeResultOfElMain"
                    >
                      <i class="fa-solid fa-xmark"></i>
                    </button>
                  </div>
                </div>

                <!-- 运行结果内容 -->
                <div class="result-contentOfElMain">
                  <!-- 模型运行结果展示区 -->
                  <div class="resultsContainer"
                       style="background-color: white;padding-bottom: 5px;height: 100%;width: 100%;overflow-y: auto;">
                    <!-- 显示程序运行的进度条 -->
                    <div v-if="processing"
                         style="display: flex; justify-content: center; align-items: center; padding-top: 120px;">
                      <span style="font-weight: 700; font-size: 22px">程序正在运行中</span>
                      <el-progress :percentage="percentage" :indeterminate="true"/>
                    </div>

                    <!-- 点击在可视化建模区展示算法的具体介绍 -->
                    <div style="width: 100%; height: 100%; background-color: white;"
                         v-if="(showPlainIntroduction || showStatusMessage) && !processing">
                      <el-scrollbar height="480px" style="background-color: white;">
                        <a-button type="text" style="position: absolute; top: 5px; right: 5px"
                                  v-if="showPlainIntroduction"
                                  @click="showPlainIntroduction = false">关闭
                        </a-button>
                        <v-md-preview v-if="showPlainIntroduction" :text="introductionToShow"
                                      style="text-align: left;"></v-md-preview>
                        <v-md-preview v-if="showStatusMessage" :text="statusMessageToShow"
                                      style="text-align: center; padding-top: 80px"></v-md-preview>
                      </el-scrollbar>
                    </div>

                    <!-- 结果可视化区默认为自定义建模或是预定义模型的使用介绍 -->
                    <div
                        v-if="!showPlainIntroduction && !showStatusMessage && !canShowResults && !contrastVisible && !processing"
                        style="background-color: white; height: 100%; width: auto; font-family: 'Microsoft YaHei';">
                      <el-scrollbar height="100%">
                        <!-- 自定义建模 -->
                        <div v-if="(userRole==='superuser' || userRole === 'user') && modelSelection === 'customModel'">
                          <v-md-preview
                              :text="howToCustomizeModel"
                              style="text-align: left;"
                              v-if="(userRole==='superuser')"
                              > </v-md-preview>
                          <div v-if="(userRole==='superuser')">
                            <div style="text-align: left; padding-left: 40px;">
                              <h4>1.机器学习的故障诊断流程推荐</h4>
                              <img src="../assets/customize-model-1.png" width="900px" alt="">
                              <!-- <div>模版用例：
                                <a-button @click="useModel(predefinedModel['templateModel1'])">用例1</a-button>
                                <a-button>用例2</a-button>
                              </div> -->
                              <br>
                              <h4>2.深度学习的故障诊断流程推荐</h4>
                              <img src="../assets/customize-model-2.png" width="600px" alt="">
                              <!-- <div>模版用例：
                                <a-button @click="useModel(predefinedModel['templateModel1'])">用例1</a-button>
                                <a-button>用例2</a-button>
                              </div> -->
                            </div>
                          </div>

                        </div>
                        <!-- 预定义模型 -->
                        <div v-if="userRole === 'superuser' && modelSelection === 'templateModel'">
                          <v-md-preview :text="howToUseTemplateModel" style="text-align: left;"></v-md-preview>
                        </div>
                        <div v-if="userRole === 'user' && modelSelection === 'templateModel'">
                          <v-md-preview :text="howToUseTemplateModel2" style="text-align: left;"></v-md-preview>
                        </div>
                      </el-scrollbar>
                    </div>

                    <!-- 当点击二级目录后，展示二级目录下各个算法的优劣比较 -->
                    <div v-if="contrastVisible && !processing"
                         style="background-color: white; height: 100%; width: auto; position: relative;">
                      <el-scrollbar height="570px" style="background-color: white;">
                        <a-button type="text" style="position: absolute; top: 5px; right: 5px"
                                  @click="contrastVisible = false">
                          关闭
                        </a-button>
                        <v-md-preview :text="contrastToShow" style="text-align: left;"></v-md-preview>
                      </el-scrollbar>
                    </div>

                    <!-- 显示结果 -->
                    <el-scrollbar height="100%" v-show="canShowResults && !processing" v-if="canShowResults && !processing" style="background-color: white;">
                      <!-- 健康评估可视化 -->
                      <!-- 不同样本的评估结果 -->
                      <div v-show="displayHealthEvaluation" v-if="displayHealthEvaluation || generateHealthEvaluationFigure">
                        <div v-show="showResultSs==='总结论'">
                          <div style="display:flex; flex-direction: row; align-items: center;">
                            <div id="healthEvaluationPieChart" style="width: 600px; height: 500px"></div>
                            <div style="width: 700px;">
                              <el-text style="font-weight: bold; font-size: 18px;">{{
                                  finalSuggestion
                                }}
                              </el-text>
                            </div>
                            <!-- 绘制饼状图 -->
                          </div>
                        </div>
                        <div v-show="showResultSs==='详情'">
                          <el-tabs type="border-card" tab-position="top" v-model="healthEvaluationOfExample"
                                   v-show="displayHealthEvaluation" v-if="displayHealthEvaluation || generateHealthEvaluationFigure">
                            <el-tab-pane v-for="(value, key) in resultsBarOfAllExamples" :key="key" :label="key"
                                         :name="key">
                              <el-tabs type="border-card" tab-position="left" v-model="activeName1">
                                <el-tab-pane label="层级有效指标" name="first">
                                  <!-- <img :src="healthEvaluationFigure1" alt="figure1" id="health_evaluation_figure_1"
                                    class="result_image" style="width: auto; height: 450px;" /> -->
                                  <el-image
                                      style="width: auto; height: 450px;"
                                      :src="resultsBarOfAllExamples[key]"
                                      :zoom-rate="1.2"
                                      :max-scale="7"
                                      :min-scale="0.2"
                                      :preview-src-list="[resultsBarOfAllExamples[key]]"
                                      :initial-index="4"
                                      fit="cover"
                                  />
                                </el-tab-pane>
                                <el-tab-pane label="指标权重" name="second">
                                  <!-- <img :src="healthEvaluationFigure2" alt="figure2" id="health_evaluation_figure_2"
                                    class="result_image" style="width: auto; height: 450px;" /> -->
                                  <el-image
                                      style="width: auto; height: 450px;"
                                      :src="levelIndicatorsOfAllExamples[key]"
                                      :zoom-rate="1.2"
                                      :max-scale="7"
                                      :min-scale="0.2"
                                      :preview-src-list="[levelIndicatorsOfAllExamples[key]]"
                                      :initial-index="4"
                                      fit="cover"
                                  />
                                </el-tab-pane>
                                <el-tab-pane label="评估结果" name="third">
                                  <div
                                      style="display:flex; flex-direction: column; justify-content: center; align-items: center; width: 100%; height: 100%">
                                    <el-image
                                        style="width: 800px; height: auto;"
                                        :src="statusOfExamples[key]"
                                        :zoom-rate="1.2"
                                        :max-scale="7"
                                        :min-scale="0.2"
                                        :preview-src-list="[statusOfExamples[key]]"
                                        :initial-index="4"
                                        fit="cover"
                                    />
                                    <br>
                                    <div style="width: 700px;">
                                      <el-text :v-model="suggestionOfAllExamples[key]"
                                               style="font-weight: bold; font-size: 18px;">
                                        {{
                                          suggestionOfAllExamples[key]
                                        }}
                                      </el-text>
                                    </div>
                                  </div>
                                  <!-- <img :src="healthEvaluationFigure3" alt="figure3" id="health_evaluation_figure_3"
                                    class="result_image" style="width: auto; height: 360px;" /> -->
                                </el-tab-pane>
                              </el-tabs>
                            </el-tab-pane>
                          </el-tabs>
                        </div>
                      </div>


                      <!-- 特征提取可视化 -->
                      <div v-if="displayFeatureExtraction || generateFeatureExtractionFigure" v-show="displayFeatureExtraction && missionComplete" style="justify-content: center;">
                        <el-tabs tab-position="left" type="border-card" v-model="featuresExtractionRawData">
                          <el-tab-pane v-for="item in rawDataList" :key="item.snesor_no" :label="item.sensor_no"
                                       :name="item.sensor_no">
                            <div :id="item.sensor_no" style="width: 1300px; height: 400px;"></div>
                            <!-- <div style="padding-left: 10px;text-align: left; font-size: 25px; color:darkgrey;">由原始信号提取特征：</div> -->
                            <!-- 对应特征提取结果 -->
                            <div :id="item.sensor_no + 'features'" style="width: 1300px; height: 400px;"></div>
                          </el-tab-pane>
                        </el-tabs>
                      </div>

                      <!-- 特征选择可视化 -->
                      <div v-show="displayFeatureSelection && missionComplete" v-if="displayFeatureSelection || generateFeatureSelectionFigure">
                        <!-- <el-tabs v-model="featuresSelectionTabs">
                          <el-tab-pane label="特征选择结果" name="first"> -->
                          <div v-show="showResultSs==='特征选择结果'">
                            <el-scrollbar height="480px">
                              <el-image
                                  style="width: auto; height: 430px;"
                                  :src="featureSelectionFigure"
                                  :zoom-rate="1.2"
                                  :max-scale="7"
                                  :min-scale="0.2"
                                  :preview-src-list="[featureSelectionFigure]"
                                  :initial-index="4"
                                  fit="cover"
                              />
                              <br>
                              <div style="width: 1000px; margin-left: 250px;">
                                <span style="font-weight: bold; font-size: 15px;">根据规则：{{ selectFeatureRule }}，选取特征结果为： {{
                                  featuresSelected
                                }}</span>
                              </div>
                            </el-scrollbar>


                            
                          </div>
                          <div v-show="showResultSs==='相关系数矩阵热力图'">
                            <el-scrollbar height="480px">
                              <el-image
                                  style="width: auto; height: 500px;"
                                  :src="correlationFigure"
                                  :zoom-rate="1.2"
                                  :max-scale="7"
                                  :min-scale="0.2"
                                  :preview-src-list="[correlationFigure]"
                                  :initial-index="4"
                                  fit="cover"
                              />
                            </el-scrollbar>
                          </div>

                      </div>

                      <!-- 故障诊断可视化 -->
                      <div v-if="displayFaultDiagnosis || generateFaultDiagnosisFigure" v-show="displayFaultDiagnosis && missionComplete" class="result-visualization-container">
                        <v-md-preview style="padding: 0px; margin: 0px"
                                      :text="faultDiagnosisResultsText"></v-md-preview>
                        
                        <!-- 用户反馈对话框 -->
                        <div style="width: 100%; position: relative; z-index: 999;">
                          <span style="position: absolute; right: 30px; top: 55px;">
                            <a-button circle :icon="h(EditOutlined)"
                            @click="feedBackDialogVisible = true" ></a-button> 反馈
                          </span>
                          <a-modal v-model:open="feedBackDialogVisible" title="用户反馈" cancelText="取消" okText="提交" @ok="feedBack">
                            <div style="font-weight: 600; font-size: 14px; margin-bottom: 20px">
                              <p>当前使用的模型：{{ modelLoadedName }}</p>
                              <p>当前使用的数据：{{ usingDatafile }}</p>
                            </div>
                            <a-form :model="feedBackFormRefState" :rules="feedBackRules" ref="feedBackFormRef">
                              <a-form-item label="当前模型中存在疑问的模块" name="module">
                                <a-select style="width: 70%" placeholder="请选择组件" v-model:value="feedBackFormRefState.module">
                                  <a-select-option v-for="item in contentJson.modules" :value="item">
                                    {{ item }}
                                  </a-select-option>
                                </a-select>
                              </a-form-item>
                              <a-form-item name="feedbackContent">
                                <div>问题描述</div>
                                <a-input style="width: 80%" v-model:value="feedBackFormRefState.feedbackContent"/>
                              </a-form-item>
                              <!-- <a-form-item>
                                <a-button @click="feedBack"></a-button>
                              </a-form-item> -->
                            </a-form>
                          </a-modal>
                        </div>
                        <div   v-show="showResultSs==='连续样本指标变换'">
                          <div id="indicatorVaryingFigure" style="width: 1200px; height: 500px"></div>
                        </div>
                        <div  v-show="showResultSs==='不同类型样本占比'">
                          <!-- 故障样本与非故障样本数量饼状图 -->
                          <div id="faultExampleRatioFigure" style="width: 1200px; height: 500px"></div>
                        </div>
                        <div  v-if="showResultSs==='原始信号波形图'">
                          <div style="width: 1200px; height: 500px">
                            <el-image
                                style="width: auto; height: 450px;"
                                :src="faultDiagnosisFigure"
                                :zoom-rate="1.2"
                                :max-scale="7"
                                :min-scale="0.2"
                                :preview-src-list="[faultDiagnosisFigure]"
                                :initial-index="4"
                                fit="cover"
                            />
                          </div>
                        </div>
<!--                        <el-tabs v-model="faultDiagnosisResultOption" tab-position="top">-->
<!--                        -->
<!--&lt;!&ndash;                          <el-tab-pane key="1" label="连续样本指标变化" v-if="canShowIndicator">&ndash;&gt;-->
<!--&lt;!&ndash;                            &lt;!&ndash; 连续样本指标变化的折线图 &ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;                            <div id="indicatorVaryingFigure" style="width: 1200px; height: 500px"></div>&ndash;&gt;-->
<!--&lt;!&ndash;                          </el-tab-pane>&ndash;&gt;-->
<!--&lt;!&ndash;                          <el-tab-pane key="2" label="不同类型样本占比">&ndash;&gt;-->
<!--&lt;!&ndash;                            &lt;!&ndash; 故障样本与非故障样本数量饼状图 &ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;                            <div id="faultExampleRatioFigure" style="width: 1200px; height: 500px"></div>&ndash;&gt;-->
<!--&lt;!&ndash;                          </el-tab-pane>&ndash;&gt;-->
<!--                          <el-tab-pane key="4" label="故障诊断结果">-->
<!--                            <div style="width: 1200px; height: 500px;display: flex; flex-direction: column; align-items: center">-->
<!--                              <span>{{ faultDiagnosisComplementarySummary }}</span>-->
<!--                              <el-image-->
<!--                                  style="width: auto; height: 450px;"-->
<!--                                  :src="faultDiagnosisComplementaryFigure"-->
<!--                                  :zoom-rate="1.2"-->
<!--                                  :max-scale="7"-->
<!--                                  :min-scale="0.2"-->
<!--                                  :preview-src-list="[faultDiagnosisComplementaryFigure]"-->
<!--                                  :initial-index="4"-->
<!--                                  fit="cover"-->
<!--                              />-->
<!--                            </div>-->
<!--                          </el-tab-pane>-->
<!--                          <el-tab-pane key="3" label="原始信号波形图">-->
<!--                            <div style="width: 1200px; height: 500px">-->
<!--                              <el-image-->
<!--                                  style="width: auto; height: 450px;"-->
<!--                                  :src="faultDiagnosisFigure"-->
<!--                                  :zoom-rate="1.2"-->
<!--                                  :max-scale="7"-->
<!--                                  :min-scale="0.2"-->
<!--                                  :preview-src-list="[faultDiagnosisFigure]"-->
<!--                                  :initial-index="4"-->
<!--                                  fit="cover"-->
<!--                              />-->
<!--                            </div>-->
<!--                          </el-tab-pane>-->
<!--                          -->
<!--                        </el-tabs>-->
                      </div>

                      <!-- 故障故障预测可视化 -->
                      <div v-show="displayFaultRegression && missionComplete"  v-if="displayFaultRegression || generateFaultRegressionFigure" style="margin-top: 20px; font-size: 18px;">
                        <div style="width: 1000px; margin-left: 250px; font-weight: bold; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                          经故障诊断算法，目前该部件<span :v-model="faultRegression"
                                                         style="font-weight: bold; color: red;">{{
                            faultRegression
                          }}</span>
                          <span v-if="!haveFault" :v-model="timeToFault" style="font-weight: bold;">根据故障预测算法预测，该部件{{
                              timeToFault
                            }}后会出现故障</span>
                        </div>
                        <br>

                        <el-image
                            style="width: auto; height: 450px;"
                            :src="faultRegressionFigure"
                            :zoom-rate="1.2"
                            :max-scale="7"
                            :min-scale="0.2"
                            :preview-src-list="[faultRegressionFigure]"
                            :initial-index="4"
                            fit="cover"
                        />
                      </div>

                      <!-- 插补可视化 -->
                      <el-tabs v-model="activeName3" v-show="displayInterpolation && missionComplete" v-if="displayInterpolation || generateInterpolationFigure" type="border-card">
                        <el-tab-pane v-for="item in interpolationResultsOfSensors" :key="item.name" :label="item.label"
                                     :name="item.name">
                          <el-image
                              style="width: auto; height: 450px;"
                              :src="interpolationFigures[item.name - 1]"
                              :zoom-rate="1.2"
                              :max-scale="7"
                              :min-scale="0.2"
                              :preview-src-list="[interpolationFigures[item.name - 1]]"
                              :initial-index="4"
                              fit="cover"
                          />
                        </el-tab-pane>
                      </el-tabs>

                      <!-- 无量纲化可视化 -->
                      <div v-show="displayNormalization && missionComplete" v-if="displayNormalization || generateNormalizationFigure" style="font-size: 18px;">
                        <!-- 针对提取到的特征进行的无量纲化得到的结果 -->
                        <div v-if="normalizationResultType == 'table'">
                          <div style="font-size: large;">原数据</div>
                          <el-table :data="normalizationFormdataRaw" style="width: 96%; margin-top: 20px;"
                          >
                            <el-table-column v-for="column in normalizationColumns" :key="column.prop"
                                             :prop="column.prop"
                                             :label="column.label"
                                             :width="column.width">
                            </el-table-column>
                          </el-table>
                          <br>
                          <div style="font-size: large;">标准化后数据</div>
                          <el-table :data="normalizationFormdataScaled" style="width: 96%; margin-top: 20px;"
                          >
                            <el-table-column v-for="column in normalizationColumns" :key="column.prop"
                                             :prop="column.prop"
                                             :label="column.label"
                                             :width="column.width">
                            </el-table-column>
                          </el-table>
                        </div>
                        <!-- 针对原始信号序列进行无量纲化得到的结果 -->
                        <el-tabs v-model="activeName4" v-if="normalizationResultType == 'figure'" type="border-card">
                          <el-tab-pane v-for="item in normalizationResultsSensors" :key="item.name" :label="item.label"
                                       :name="item.name">
                            <el-image
                                style="width: 900; height: 450px;"
                                :src="normalizationResultFigures[item.name - 1]"
                                :zoom-rate="1.2"
                                :max-scale="7"
                                :min-scale="0.2"
                                :preview-src-list="[normalizationResultFigures[item.name - 1]]"
                                :initial-index="4"
                                fit="cover"
                            />
                          </el-tab-pane>
                        </el-tabs>

                      </div>

                      <!-- 小波降噪可视化 -->
                      <!-- <img :src="denoiseFigure" alt="denoise_figure" class="result_image"
                        style="width: 900px; height: 450px;" /> -->
                      <el-tabs v-model="activeName2" v-show="displayDenoise && missionComplete" v-if="displayDenoise || generateDenoiseFigure"  type="border-card">
                        <el-tab-pane v-for="item in waveletResultsOfSensors" :key="item.name" :label="item.label"
                                     :name="item.name">
                          <el-image
                              style="width: auto; height: 450px;"
                              :src="denoiseFigures[item.name - 1]"
                              :zoom-rate="1.2"
                              :max-scale="7"
                              :min-scale="0.2"
                              :preview-src-list="[denoiseFigures[item.name - 1]]"
                              :initial-index="4"
                              fit="cover"
                          />
                        </el-tab-pane>
                      </el-tabs>
                      <!-- 展示用户文件中原始数据 -->
                      <div v-if="displayRawDataWaveform" style="padding: 20px; position: relative;">
                        <el-button text
                                   style="color: green;position: absolute; right: 10px; top: 10px; width: 90px; height: 50px"
                                   @click="displayRawDataWaveform = false">关闭
                        </el-button>
                        <p style="text-align: left; color: red; font-weight: bolder; font-size: 18px">
                          已上传数据文件内容浏览</p>
                        <p style="font-size: 18px">文件名：{{ currentDataBrowsing }}</p>
                        <el-image
                            style="width: auto; height: 450px;"
                            :src="rawDataWaveform"
                            :zoom-rate="1.2"
                            :max-scale="7"
                            :min-scale="0.2"
                            :preview-src-list="[rawDataWaveform]"
                            :initial-index="4"
                            fit="cover"
                        />

                      </div>
                    </el-scrollbar>
                  </div>
                </div>
              </div>
            </transition>

            <!-- 控制按钮 -->
            <div class="control-buttonsOfElMain">
              <button
                  class="icon-buttonOfElMain"
                  :style="dark ? 'color: #ffffff;' : 'color: #000000;'"
                  @click="showResultOfElMain"
                  v-if="!isResultVisibleOfElMain"
                  aria-label="显示结果"
                  @keydown.enter.prevent="showResultOfElMain"
                  @keydown.space.prevent="showResultOfElMain"
              >
                <i class="fa-solid fa-angles-up"></i>
              </button>
            </div>


            <!-- 输出结果配置面板 -->
            <el-dialog v-model="outputConfigVisible" title="模型输出" style="width: 40%; min-height: 30%">
              <div style="display: flex; flex-direction: column; justify-content: left;">
                  <!-- <span style="">选择需要输出的结果</span>
                  <el-check-group v-model="moduleResultToGenerateList">
                    <el-checkbox v-for="node in nodeList" :key="node.id" :label="node.label" :value="node.label"/>
                  </el-check-group> -->
                <div
                  style="
                    padding: 30px;
                    display: flex;
                    flex-direction: row;
                    align-items: center;
                    font-family: 'Microsoft YaHei';
                    font-size: 17px
                  "
                >
                  <span>
                    <p>选择需要输出的结果：<br/>（至少选择一项）</p>
                  </span>
                  
                  
                  <div style="max-width: 50%; margin-left: 30px">
                    <el-checkbox
                      v-model="selectAllModuleToGenerateResult"
                      @change="toggleSelectAll"
                      style=""
                      >全选</el-checkbox
                    >
                  
                    <el-checkbox-group v-model="moduleResultToGenerateList" :min="1">
                    <!--  -->
                      <el-checkbox size="large" v-for="module in contentJson.modules" :key="module" :label="module" :value="module"/>
                    </el-checkbox-group>
                  </div>
                </div>
                <div style="margin-top: 50px">
                  <el-button style="width: 180px; font-size: 17px" type="primary" @click="generateConclusion">生成输出报告</el-button>
                 
                </div>
              </div>
            </el-dialog>
          </div>
        </el-main>
    
        <!-- 以抽屉的形式打开用户历史数据 -->
        <!-- <el-drawer v-model="dataDrawer" direction="ltr" size="45%">
          <div style="display: flex; flex-direction: column">
            <el-col>
              <h2 style="margin-bottom: 25px; color: #253b45">用户数据文件</h2>

              <el-table :data="fetchedDataFiles" height="500" stripe style="width: 100%">
                <el-table-column :width="100" property="owner" label="文件上传者" show-overflow-tooltip/>
                <el-table-column :width="200" property="dataset_name" label="文件名称" show-overflow-tooltip/>
                <el-table-column :width="230" property="description" label="文件描述" show-overflow-tooltip/>
                <el-table-column :width="210" label="操作">
                  <template #default="scope">
                    <el-button
                        size="small"
                        type="primary"
                        style="width: 50px"
                        @click="useDataset(scope.row)"
                        :loading="loadingData"
                    >
                      使用
                    </el-button>
                    <el-popconfirm title="你确定要删除该数据文件吗"
                                   @confirm="deleteDatasetConfirm(scope.$index, scope.row)">
                      <template #reference>
                        <el-button
                            size="small"
                            type="danger"
                            style="width: 50px"
                        >
                          删除
                        </el-button>
                      </template>
                      <template #actions="{ confirm, cancel }">
                        <el-row>
                          <el-col :span="12">
                            <el-button size="small" @click="cancel">取消</el-button>
                          </el-col>
                          <el-col :span="12">
                            <el-button
                                type="primary"
                                size="small"
                                @click="confirm"
                            >
                              确定
                            </el-button>
                          </el-col>
                        </el-row>
                      </template>
                    </el-popconfirm>

                    <el-button
                        size="small"
                        type="success"
                        style="width: 50px"
                        @click="browseDataset(scope.row)"
                    >
                      查看
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-col>

          </div>

        </el-drawer> -->
      </el-container>
    </el-container>

    <a-modal
        v-model:open="dialogModle"
        title="保存模型" width="30%"
        footer=""
    >
      <el-form
          :model="modelInfoForm"
          :rules="rules"
          ref="modelInfoFormRef">
        <el-form-item
            label="模型名称"
            :label-width='140'
            prop="name"
        >
          <el-input
              style="width: 200px;"
              v-model="modelInfoForm.name"
              autocomplete="off"/>
        </el-form-item>
          
        <el-form-item 
          label="模型描述" 
          :label-width='140' 
          prop="description"
        >
          <el-input style="width: 200px;" v-model="modelInfoForm.description"/>
        </el-form-item>

        <!-- 选择挂载的类型-->

        <el-form-item
            label="适配部件"
            :label-width='140'
            prop="classify"
        >
          <a-tree-select
              v-model:value="modelInfoForm.class"
              show-search
              style="width: 200px"
              :dropdown-style="{ maxHeight: '400px', overflow: 'auto' }"
              placeholder="请选择适配部位分类"
              allow-clear
              :tree-data="filteredDataSource"
              tree-node-filter-prop="label"
              @select="handleSelectType"
          >
            <template #title="{ value: val, label }">
              <!-- <b v-if="val === 'parent 1-1'" style="color: #08c">unknown</b> -->
              <span>{{ label }}</span>
            </template>
          </a-tree-select>
        </el-form-item>
      </el-form>
      <span class="dialog-footer">
        <el-button style="margin-left: 85px; width: 150px;" @click="dialogModle = false">取消</el-button>
        <el-button style="width: 150px;" type="primary" @click="saveModelConfirm(modelInfoFormRef)">确定</el-button>
      </span>
    </a-modal>
  </div>
</template>

<script lang="ts" setup>

import {computed, h, nextTick, onMounted, reactive, ref, watch} from 'vue'
import {jsPlumb} from 'jsplumb'
import {Action, ElButton, ElDialog, ElInput, ElMessage, ElMessageBox, ElNotification, ElTree} from "element-plus";
import axios from 'axios';
import {useRouter} from 'vue-router';
import api from '../utils/api.js'
import {
  contrastOfAlgorithm,
  labelsForAlgorithms,
  labelsForParams,
  plainIntroduction,
  predefinedModel
} from '../components/constant.ts'
import * as echarts from 'echarts';
import {
  EditOutlined,
  FolderOpenOutlined,
  FolderOutlined,
  QuestionCircleOutlined,
  UploadOutlined
} from "@ant-design/icons-vue";
import ComponentTree from './ComponentTree.vue';
import type {UploadProps} from "ant-design-vue";
import {message} from "ant-design-vue";
import {Rule} from "ant-design-vue/es/form";
import uploadPrivateAlgorithmFiless from '../components/uploadPrivateAlgorithmFiles.vue'
import managePrivateAlgorithm from '../components/managePrivateAlgorithm.vue';

///////////////////////////////////////////////////////////////////////////////sidebar start
//菜单相关
import MyCollapse from "../components/MyCollapse.vue"
import MyCollapseItem from "../components/MyCollapseItem.vue"
//拖拽组件相关
import DragModelItem from "./DragModelItem.vue"
import type Node from 'element-plus/es/components/tree/src/model/node'
//////////////////////////////////////////////////////////////////模型管理相关
import PublishModel from './PublishModel.vue';
//////////////////////////////////////////////////////////////////用户数据编辑相关
import datasetManagement from './datasetManagement.vue';
//////////////////////////////////////////////////////////////////系统组件源码编辑相关
import editCodeEmbedded from './editCodeEmbedded.vue';


// 选中类型，返回id
// const handleSelectType = (value, node, extra)=>{
//   console.log("handleSelectType value: ", value)
//   console.log("handleSelectType node: ", node)
// }

//模型管理
// 当子组件删除模型，并且该模型已经被加载，则需要重置模型
const handleResetModel = (modelName: string) => {
  if (modelLoaded.value == modelName) {
    modelLoaded.value = '无'
    modelHasBeenSaved = false
    canStartProcess.value = true
    handleClear()
  }
}

let modelLoadedName = ref(''); // 已加载模型的名称
// 点击子组件publishModel的历史模型表格中使用按钮复现用户历史模型
const handleLoadModel = (store: any) => {
  console.log('接受子组件数据',store)
  // modelLoaded.value = store.valmodelName
  //后端传来的数据恢复画布信息
  console.log('store.modelInfo.model_info: ', store.value.modelInfo[0].model_info)
  let objects = JSON.parse(store.value.modelInfo[0].model_info)
  //要执行两遍才会渲染上
  restoreCanvas(objects)
  // 使用setTimeout等待0.5秒
  setTimeout(() => {
    // 0.5秒后执行的操作
    restoreCanvas(objects)
  }, 500);

  handleClear()
  updateStatus('当前模型已保存')
  modelHasBeenSaved = true
  modelHasBeenChecked.value = true
  canStartProcess.value = false
  modelLoaded.value = store.value.modelName
  modelLoadedName.value = store.value.modelName
  modelLoadedId = String(store.value.modelId)
  console.log("modelLoaded: ", modelLoaded.value)
  console.log("modelLoadedId: ", modelLoadedId)

}
// 用户查看源文件
const browseDataset = (row: { dataset_name: any; }) => {

// 清除可视化区域内容
resultsViewClear()
canShowResults.value = true
// 发送请求获取原始数据的波形图
let filename = row.dataset_name

api.get('user/browse_datafile/?filename=' + filename).then((response: any) => {
  if (response.status === 200) {
    displayRawDataWaveform.value = true
    let data = response.data
    let figure = data.figure_Base64

    rawDataWaveform.value = 'data:image/png;base64,' + figure
    currentDataBrowsing.value = filename
    console.log('访问成功：')
  } else {
    ElMessage.error('访问文件失败')
  }
})
    .catch((error: any) => {
      console.log('访问文件失败：', error)
    })
}
// 修改模型源码
const canOpenCodeEditor = ref(true)
let moduleWithCode: string[] = []
const codeEditDialogVisible = ref(false)

const openCodeEditPanel = () => {
  codeEditDialogVisible.value = true
}
// 用户选择数据库中的数据集
const datasetManagementDialog = ref(false)
const searchDataKeyword = ref('')
// 子组件向父组件发送数据
// const emit = defineEmits(["switchDrawer"]);
const openDatasetLoadingPanel = () => {
  let url = 'user/fetch_datafiles/'
  api.get(url)
      .then((response: any) => {
        let datasetInfo = response.data
        modelsDrawer.value = false;
        fetchedDataFiles.value = []
        
        for (let item of datasetInfo) {
          fetchedDataFiles.value.push(item)
        }
        
        // dataDrawer.value = true
        datasetManagementDialog.value = true
        // emit("switchDrawer", fetchedDatasetsInfo);
      })

  // fetchData.forEach(element => {
  //   fetchedDataFiles.value.push(element)
  // });

};
//////////////////////////////////////////////////////////////////菜单面板--start
const activeNamesOfMenuPanel = ref(['1'])// 当前展开项


//点击菜单项
const onItemClickOfMycollapse = (data: any) => {

}
//////////////////////////////////////////////////////////////////菜单面板--end
///////////////////////////////////////////////////////////////////////////////sidebar end

///////////////////////////////////////////////////////////////////////////////树--start

/////////////////////////////////////////////////////////////////////////////////树end

///////////////////////////////////////////////////////////////////////////////el-main分割start
//onMounted中还有相关的初始化方法
import {onBeforeUnmount} from 'vue'
import throttle from 'lodash/throttle'
// 控制运行结果区域的显示与隐藏
const isResultVisibleOfElMain = ref(true)
const resultHeightOfElMain = ref(window.innerHeight / 2) // 默认高度
const previousHeightOfElMain = ref(resultHeightOfElMain.value)
// 拖动调整高度
const MIN_HEIGHT_OF_EL_MAIN = 30
let MAX_HEIGHT_OF_EL_MAIN = window.innerHeight - 60

let startYOfElMain = 0
let startHeightOfElMain = 0
let draggingOfElMain = false

// const toggleResultOfElMain = () => {
//   if (isResultVisibleOfElMain.value) {
//     // 保存当前高度
//     previousHeightOfElMain.value = resultHeightOfElMain.value
//   }
//   isResultVisibleOfElMain.value = !isResultVisibleOfElMain.value
// }

//开启结果显示区域
const showResultOfElMain = () => {
  resultHeightOfElMain.value = previousHeightOfElMain.value
  isResultVisibleOfElMain.value = true
}

//关闭结果显示区域
const closeResultOfElMain = () => {
  if (isResultVisibleOfElMain.value) {
    previousHeightOfElMain.value = resultHeightOfElMain.value
    isResultVisibleOfElMain.value = false
  }
}

// 初始化拖动（鼠标）
const initDragOfElMain = (event) => {
  event.preventDefault()
  startYOfElMain = event.clientY
  startHeightOfElMain = resultHeightOfElMain.value
  draggingOfElMain = true
  window.addEventListener('mousemove', onDragOfElMain)
  window.addEventListener('mouseup', stopDragOfElMain)
}

// 初始化拖动（触摸）
const initDragTouchOfElMain = (event) => {
  event.preventDefault()
  if (event.touches.length !== 1) return
  startYOfElMain = event.touches[0].clientY
  startHeightOfElMain = resultHeightOfElMain.value
  draggingOfElMain = true
  window.addEventListener('touchmove', onDragTouchOfElMain, {passive: false})
  window.addEventListener('touchend', stopDragOfElMain)
}

// 拖动处理（鼠标）
const onDragOfElMain = throttle((event) => {
  if (!draggingOfElMain) return
  const dy = startYOfElMain - event.clientY
  const newHeight = startHeightOfElMain + dy
  if (newHeight >= MIN_HEIGHT_OF_EL_MAIN && newHeight <= MAX_HEIGHT_OF_EL_MAIN) {
    resultHeightOfElMain.value = newHeight
  }
}, 16) // 每16ms触发一次，约60fps

// 拖动处理（触摸）
const onDragTouchOfElMain = throttle((event) => {
  if (!draggingOfElMain) return
  if (event.touches.length !== 1) return
  event.preventDefault()
  const dy = startYOfElMain - event.touches[0].clientY
  const newHeight = startHeightOfElMain + dy
  if (newHeight >= MIN_HEIGHT_OF_EL_MAIN && newHeight <= MAX_HEIGHT_OF_EL_MAIN) {
    resultHeightOfElMain.value = newHeight
  }
}, 16)

// 停止拖动
const stopDragOfElMain = () => {
  draggingOfElMain = false
  window.removeEventListener('mousemove', onDragOfElMain)
  window.removeEventListener('mouseup', stopDragOfElMain)
  window.removeEventListener('touchmove', onDragTouchOfElMain)
  window.removeEventListener('touchend', stopDragOfElMain)
}

// 更新最大高度
const updateMaxHeightOfElMain = () => {
  MAX_HEIGHT_OF_EL_MAIN = window.innerHeight - 60
  if (resultHeightOfElMain.value > MAX_HEIGHT_OF_EL_MAIN) {
    resultHeightOfElMain.value = MAX_HEIGHT_OF_EL_MAIN
  }
  if (previousHeightOfElMain.value > MAX_HEIGHT_OF_EL_MAIN) {
    previousHeightOfElMain.value = MAX_HEIGHT_OF_EL_MAIN
  }
}

// 创建一个节流版本的handleResize函数，每100毫秒最多执行一次，优化
const throttledHandleResize = throttle(updateMaxHeightOfElMain, 100);


onBeforeUnmount(() => {
  window.removeEventListener('mousemove', onDragOfElMain)
  window.removeEventListener('mouseup', stopDragOfElMain)
  window.removeEventListener('touchmove', onDragTouchOfElMain)
  window.removeEventListener('touchend', stopDragOfElMain)
  window.removeEventListener('resize', throttledHandleResize);
  // window.removeEventListener('resize', updateMaxHeightOfElMain)
  // window.removeEventListener('beforeunload', saveStateOfElMain)
})
///////////////////////////////////////////////////////////////////////////////el-main分割end

///////////////////////////////////////////////////////////////////////////////建模区start
import {MarkerType, Panel, Position, useVueFlow, VueFlow} from '@vue-flow/core'
// import {Background} from '@vue-flow/background'
import {ControlButton, Controls} from '@vue-flow/controls'
import Icon from '../components/vueflow/Icon.vue'
import DragDropzoneBackground from '../components/vueflow/DragDropzoneBackground.vue'
import ModelingCustomNode from '../components/vueflow/ModelingCustomNode.vue'
import ModelingCustomEdge from "../components/vueflow/ModelingCustomEdge.vue";
import {initialEdges, initialNodes, initialNodes2} from './vueflow/initial-elements.js'

const {onInit, onNodeDragStop, onConnect, addEdges, addNodes, setViewport, toObject,removeEdges} = useVueFlow()
const {screenToFlowCoordinate, onNodesInitialized, updateNode, getNodes, getEdges, fromObject} = useVueFlow()
//节点
// const modeling_nodes = ref(initialNodes)
// const modeling_nodes2 = ref(initialNodes2)
// const modeling_nodeList = ref([])
const modeling_nodeList = ref([])

//边
// const modeling_edges = ref(initialEdges)
const modeling_edgesList = ref([])
//暗黑模式
const dark = ref(false)

onInit((vueFlowInstance) => {
  // instance is the same as the return of `useVueFlow`
  vueFlowInstance.fitView()
})

onNodeDragStop(({event, nodes, node}) => {
  // console.log('Node Drag Stop', {event, nodes, node})
})

//连接时触发
onConnect((connection) => {
  console.log('Connection Connected', {connection})
  connection.type = 'button'
  connection.animated = true
  connection.markerEnd = MarkerType.ArrowClosed
  connection.data = {
    text: 'custom edge',
  }
  connection.style = {}
  addEdges(connection)
})

//需要交互锁定
const removeBtnDisabled = ref(false)

function onInteractionChangeOfControls(active) {
  console.log("onInteractionChangeOfControls执行了...")
  console.log(active)
  removeBtnDisabled.value = active;
}

//TODO 随机打乱可能需要修改一下
function modeling_updatePos() {
  if (modeling_nodeList && modeling_nodeList.value.length > 0) {
    modeling_nodeList.value = modeling_nodeList.value.map((node) => {
      return {
        ...node,
        position: {
          x: Math.random() * 400,
          y: Math.random() * 400,
        },
      }
    })
  }
}

//TODO测试：在console输出边和节点的信息
function modeling_test_logToObject() {
  console.log(toObject())
}

//TODO测试：保存建模区的节点信息到localStorage
function modeling_test_onSave() {
  localStorage.setItem("saveKeyOfNodeInfo", JSON.stringify(toObject()))
}

//TODO测试：恢复建模区的节点信息从localStorage
function modeling_test_onRestore() {
  const flow = JSON.parse(localStorage.getItem("saveKeyOfNodeInfo"))
  if (flow) {
    fromObject(flow)
  }
}

//重置坐标到(0,0)
function modeling_resetTransform() {
  setViewport({x: 0, y: 0, zoom: 1})
}

//切换深色模式
function modeling_toggleDarkMode() {
  dark.value = !dark.value
}

//侧边栏拖拽组件后，根据拖拽组件的信息获取要渲染的节点
function getModelingNode(algorithm, node, nodeDataInfo) {
  // console.log("生成边",node)
  // console.log("生成边",nodeDataInfo)
  // console.log("生成边",algorithm)
  // if
  return {
    id: node.id + '-' + nodeDataInfo.use_algorithm,
    type: 'menu',
    // data: {label: nodeDataInfo.label_display, toolbarPosition: Position.Top},
    data: {label: nodeDataInfo.label_display, toolbarPosition: Position.Top,laglabel: nodeDataInfo.label},
    nodeInfo: nodeDataInfo, //这个是自定义的属性，原来vueflow没有
    position: {x: 0, y: 0},
    class: 'light',
    style: {background: '#fff', borderRadius: '0px',},
  };
}

//新增节点
let dd_newNode = {}
const stateOfDragNode = {
  draggedType: ref(null),
  isDragOver: ref(false),
  isDragging: ref(false),
}

const {draggedType, isDragOver, isDragging} = stateOfDragNode

watch(isDragging, (dragging) => {
  document.body.style.userSelect = dragging ? 'none' : ''
})

// 参数编辑栏对应算法编辑内容
const showParameterEdit = ref('')
const algorithm = ref('')
let item = reactive({})
const findIndex = ref(null)
//参数字典
const parameter_dict = ref({})
const model_model = reactive([])
// const dragEnd = ref(false)
//which_init_method: 就是指的那个方法初始化的节点：handleDragend | handleDragendAdd
function onDragStart(event, algorithms, node, which_init_method, type) {
  let algorithm = algorithms
  showParameterEdit.value = node.id
  if (which_init_method == "handleDragend") {
    const evClientX = event.clientX
    const evClientY = event.clientY
    let left
    if (evClientX < 300)
      left = evClientX + 'px'
    else
      left = evClientX - 300 + 'px'
    let top = 50 + 'px'
    const nodeId = node.id
    const nodeInfo = {
      label_display: labelsForAlgorithms[algorithm],   // 具体算法的名称
      label: node.label,      // 算法模块名称，例如：插值处理
      id: node.id, // 例如：插值处理的id=>1.1
      nodeId,
      nodeContainerStyle: {
        left: left,
        top: top,
      },
      use_algorithm: algorithm,
      parameters: node.parameters,
      optional: node.optional
    }
    // 针对时域或是频域特征给出不同的可选特征
    if (nodeInfo.label_display.indexOf('时域和频域') > -1) {
      features.value = ['均值', '方差', '标准差', '峰度', '偏度', '四阶累积量', '六阶累积量', '最大值', '最小值', '中位数', '峰峰值', '整流平均值', '均方根', '方根幅值',
        '波形因子', '峰值因子', '脉冲因子', '裕度因子', '重心频率', '均方频率', '均方根频率', '频率方差', '频率标准差', '谱峭度的均值', '谱峭度的峰度']
    } else {
      if (nodeInfo.label_display.indexOf('时域特征') > -1) {
        features.value = ['均值', '方差', '标准差', '峰度', '偏度', '四阶累积量', '六阶累积量', '最大值', '最小值', '中位数', '峰峰值', '整流平均值', '均方根', '方根幅值',
          '波形因子', '峰值因子', '脉冲因子', '裕度因子']
      } else if (nodeInfo.label_display.indexOf('频域特征') > -1) {
        features.value = ['重心频率', '均方频率', '均方根频率', '频率方差', '频率标准差', '谱峭度的均值', '谱峭度的峰度']
      }
    }

    dd_newNode = getModelingNode(algorithm, node, nodeInfo)
    item = dd_newNode.nodeInfo
  } else if (which_init_method == "handleDragendAdd") {
    // 使用find方法查找具有特定alias的对象
    const foundObject = fetchedExtraAlgorithmList.value.find(obj => obj.alias === algorithm)
    const parametersKey = Object.keys(foundObject.parameters)[0]
    // 如果找到了对象，复制其parameters的键
    if (foundObject) {
      console.log("找到的算法文件", parametersKey); // 输出: ['private_fault_diagnosis_deeplearning', 'private_fault_diagnosis_machine_learning']
    }
    
    node.parameters[parametersKey] = node.alias 
    // 拖拽进来相对于地址栏偏移量
    console.log("add增值", node)
    const evClientX = event.clientX
    const evClientY = event.clientY
    let left
    if (evClientX < 300) {
      left = evClientX + 'px'
    } else {
      left = evClientX - 300 + 'px'
    }
    let top = 50 + 'px'
    const nodeId = node.id
    const nodeInfo = {
    
      label_display: node.alias,   // 具体算法的名称
      label: node.label,      // 算法模块名称
      id: node.id,
      nodeId,
      nodeContainerStyle: {
        left: left,
        top: top,
      },
      use_algorithm: parametersKey,
      parameters: node.parameters,
      optional: node.optional
    }
    console.log("add增值1111",nodeInfo )
    // 针对时域或是频域特征给出不同的可选特征
    dd_newNode = getModelingNode(algorithm, node, nodeInfo)
    item = dd_newNode.nodeInfo
  }

  if (event.dataTransfer) {
    event.dataTransfer.setData('application/vueflow', type)
    event.dataTransfer.effectAllowed = 'move'
  }
  draggedType.value = type
  isDragging.value = true
  document.addEventListener('drop', onDragEnd)

  //TODO item = getModelingNode(algorithm, node, nodeInfo)
  

}

function onDragOver(event) {
  console.log("onDragOver执行了...")
  event.preventDefault()
  if (draggedType.value) {
    isDragOver.value = true
    if (event.dataTransfer) {
      event.dataTransfer.dropEffect = 'move'
    }
  }
 
}

function onDragLeave() {
  console.log("onDragLeave执行了...")
  
  isDragOver.value = false
}

function onDragEnd(event) {
  console.log("onDragEnd执行了...")
  isDragging.value = false
  isDragOver.value = false
  draggedType.value = null
  document.removeEventListener('drop', onDragEnd)
}

function onDrop(event) {
  console.log('drop event', event)
  //返回的是相对于建模坐标系的x,y，不是屏幕，(0,0)在初始化界面的左上角
  const position = screenToFlowCoordinate({
    x: event.clientX,
    y: event.clientY,
  })

  //调整被拖拽节点的位置到鼠标中心
  const {off} = onNodesInitialized(() => {
    updateNode(dd_newNode.id, (node) => {
      return ({
        position: {
          x: position.x - node.dimensions.width / 2,
          y: position.y - node.dimensions.height / 2
        },
      })
    })
    off()
  })

  //算法模块不允许重复
  if (modeling_nodeList.value.length > 0) {
    for (let i = 0; i < modeling_nodeList.value.length; i++) {
      if (modeling_nodeList.value[i].nodeInfo.id == dd_newNode.nodeInfo.id) {
        ElMessage({
          message: '不允许出现同一类别的算法',
          type: 'warning'
        })
        return;
      }
    }
  }
  console.log("dd_newNode.nodeInfo", dd_newNode.nodeInfo)
  modeling_nodeList.value.push(dd_newNode)
  findIndex.value = modeling_nodeList.value.findIndex(item => item.nodeInfo.id == dd_newNode.nodeInfo.id)
  console.log("索引对应的节点", dd_newNode.nodeInfo.use_algorithm)
  parameter_dict[dd_newNode.nodeInfo.use_algorithm] = findIndex.value
  console.log("索引字典", parameter_dict)
}

//节点被点击
function handleNodeClick(Props:any,action:any) {
  showResultSs.value =  action
  console.log('传入的标签',showResultSs.value)
  console.log('传入的标签',Props.data.laglabel)
  console.log("传入的值", Props.id.match( /\d+\.\d+|\d+/g)[0])
  showParameterEdit.value = Props.id.match( /\d+\.\d+|\d+/g)[0]
  let itemRusult = Props.data.laglabel
  showResult(itemRusult)
  //
  // showParameterEdit.value = event.node.nodeInfo.id
  // //运行完毕showResul
  // console.log("showParameterEdit.value",showParameterEdit.value )
  // let itemRusult = event.node.nodeInfo.label
  // console.log("itemRusult",itemRusult )
  // showResult(itemRusult);
}

// 节点间的连线改变
function handleEdgesChange(change: any) {
  console.log("handleEdgeChange", change)
  // 删除连线时，删除对应的节点
  if (change.length){
    missionComplete.value = false
    modelHasBeenChecked.value = false
    updateStatus("请建立模型并点击检查模型")
  }

  console.log("missionComplete: ", missionComplete.value)
  console.log("modelHasBeenChecked: ", modelHasBeenChecked.value)
}


//建模区域中的功能操作菜单（清空模型、检查模型...）
//控制各个按钮的disabled状态
const disabledStateOfControlBtn = ref({
  clearModelOfViewFlowBtn: false,
  finishModelOfViewFlowBtn: false,
  checkModelOfViewFlowBtn: false,
  saveModelOfViewFlowBtn: false,
  runModelOfViewFlowBtn: false,
  stopRunningModelOfViewFlowBtn: false,
  setModelConfigRunningModelOfViewFlowBtn: false,
  configPanelOfModelNodeBtn: false
})

//控制各个按钮的显示和隐藏(暂时没有使用在任何地方)
const isShowStateOfControlBtn = ref({
  clearModelOfViewFlowBtn: false,
  finishModelOfViewFlowBtn: false,
  checkModelOfViewFlowBtn: false,
  saveModelOfViewFlowBtn: false,
  runModelOfViewFlowBtn: false,
  stopRunningModelOfViewFlowBtn: false,
  setModelConfigRunningModelOfViewFlowBtn: false
})

//清空模型
function clearModelOfViewFlow() {
  modeling_nodeList.value = []
  modeling_edgesList.value = []
  showParameterEdit.value = null
  item = {}
  adjacencyList.value = [];
  inDegree.value = {};
  modelHasBeenChecked.value = false
// 排序
// 初始化顺序数组和已访问节点集合
  order.value = [];
  visited.value = new Set();
  done.value = false
  // features.value = ['均值', '方差', '标准差', '峰度', '偏度', '四阶累积量', '六阶累积量', '最大值', '最小值', '中位数', '峰峰值', '整流平均值', '均方根', '方根幅值',
  //   '波形因子', '峰值因子', '脉冲因子', '裕度因子', '重心频率', '均方频率', '均方根频率', '频率方差', '频率标准差', '谱峭度的均值', '谱峭度的标准差', '谱峭度的峰度', '谱峭度的偏度']
  jsonClear()    // 向后端发送的模型信息
  isShow.value = false
  // plumbIns.deleteEveryConnection()
  // plumbIns.deleteEveryEndpoint()
  linkedList.head = null
  linkedList.tail = null
  missionComplete.value = false // 程序处理完成
  modelSetup.value = false   // 模型设置完成
  showPlainIntroduction.value = false
  showStatusMessage.value = false
  modelHasBeenSaved = false  //复用历史模型，不做模型检查
  toRectifyModel.value = false  // 禁用修改模型
  canCompleteModeling.value = true
  canCheckModel.value = true
  canSaveModel.value = true
  processIsShutdown.value = false
  canStartProcess.value = true   // 不可运行程序
  modelLoaded.value = '无'

  updateStatus('未建立模型')

  resultsViewClear()
}

//完成模型
function finishModelOfViewFlow() {

}

//参数检查
function checkModelParam() {
  console.log("开始检查模型参数")
  console.log('模型列表', modeling_nodeList.value)
  for (let i = 0; i < modeling_nodeList.value.length; i++) {
    let dict = modeling_nodeList.value[i]
    console.log('dict.use_algorithm: ', dict.nodeInfo.use_algorithm)
    if (!dict.nodeInfo.use_algorithm) {
      return false
    } else {
      // 检查特征选择的规则参数
      if (dict.nodeInfo.id == '1.3') {
        console.log('检查到特征选择 ')
        let threshold = false
        // 检查选择特征的规则参数是否正确设置
        let rule = dict.nodeInfo.parameters[dict.nodeInfo.use_algorithm].rule
        console.log('rule: ', rule)
        if (dict.nodeInfo.parameters[dict.nodeInfo.use_algorithm]['threshold' + rule]) {
          console.log('规则参数通过: ')
          threshold = true
        }
        if (!threshold) {
          return false
        }
      } else if (dict.nodeInfo.id == '1.2') {
        // 检查特征提取参数设置

        if (!features.value.length) {
          return false
        }
      } else if(dict.nodeInfo.id == '1.4'){
         console.log('小波变换单独处理',modeling_nodeList.value)
         let parameters = dict.nodeInfo.parameters
         console.log('小波单独构建的parameters',parameters)
      }else if(dict.nodeInfo.id == '1.5'){
         console.log('无量纲单独处理',modeling_nodeList.value)
         let parameters = dict.nodeInfo.parameters
         console.log('无量纲构建的parameters',parameters)
      }else{
      // 检查一般算法模块的参数设置，参数设置不能为空
      // 
        if (!dict.nodeInfo.use_algorithm.includes('private_') && !dict.nodeInfo.use_algorithm.includes('extra_'))
          dict.nodeInfo.parameters[dict.nodeInfo.use_algorithm] = dict.nodeInfo.use_algorithm
        let parameters = dict.nodeInfo.parameters[dict.nodeInfo.use_algorithm]
        console.log('parameters: ', parameters)
        if (!parameters) {
          console.log('parameters is null')
          return false
        } else {
          for (let key in parameters) {
            if (parameters[key] === '' || parameters[key] === null) {
              console.log('parameters[key] is null: ', parameters[key])
              return false
            }
          }
        }
      }
    }
  }
  return true
}

//构建模块逻辑检查
function checkModelOrder() {
  console.log("开始检查模型逻辑")
  let idToModule = {}
  let algorithms = []
  let algorithmSchedule = []
  let moduleSchedule = []
  let moduleStr
  let algorithmStr
  //针对单个模块 逻辑上的错误检查
  console.log('content的长度', contentJson.schedule.length)

  // 判断子串后是否有更多的文本
  const moreText = (text, substring) => {
    const position = text.indexOf(substring);
    if (position === -1) {
      return false;
    }
    const endPosition = position + substring.length;
    return endPosition < text.length;
  }

  const includeHealthEvaluation = (moduleStr: string) => {
    if (moduleStr.match('层次分析模糊综合评估')) {
      return '层次分析模糊综合评估';
    } else if (moduleStr.match('层次朴素贝叶斯评估')) {
      return '层次朴素贝叶斯评估';
    } else if (moduleStr.match('层次逻辑回归评估')) {
      return '层次逻辑回归评估';
    } else if (moduleStr.match('健康评估')) {
      return '健康评估';
    } else {
      return '';
    }
  }

// 判断一个子串后是否有另一个子串，其中subStrs2为包含需要寻找的子串的数组
  const checkSubstrings = (str, subStr1, subStrs2) => {
    const index1 = str.indexOf(subStr1);
    if (index1 !== -1) {
      // 如果 subStr1 存在
      for (const subStr2 of subStrs2) {
        const index2 = str.indexOf(subStr2, index1 + subStr1.length);
        if (index2 !== -1) {
          // 如果在 subStr1 之后找到了 subStr2 中的任何一个则返回true
          return true;
        }
      }
    }
    return false;
  }

  const canRunSoloModule = (moduleStr: string, algorithmStr: string) => {
    const modulesCanRunSolo = ['插值处理', '特征提取', '小波变换', '无量纲化']

    const algorithmsCanRunSolo = [
      'GRU的故障诊断', 'LSTM的故障诊断', '一维卷积深度学习模型的故障诊断', 
      '基于时频图的深度学习模型的故障诊断', '深度学习故障诊断', '信号级加权融合的故障诊断', '信号时频表征自适应加权融合的故障诊断',
      '特征级融合的深度学习故障诊断', '决策级融合的深度学习故障诊断', '基于单传感器的知识型 1D 时域深度学习故障诊断',
      '基于单传感器的时域和频域协同注意学习故障诊断', '基于单传感器的多域深度特征融合故障诊断'
    ]
    let checkPass1 = false;
    let checkPass2 = false;
    // 检查传入的字符串中是否包含数组中任意一项，是的话返回true，否则返回false
    modulesCanRunSolo.forEach(item => {
      if (moduleStr.includes(item)) {
        checkPass1 = true
      }
    })

    algorithmsCanRunSolo.forEach(item => {
      if (algorithmStr.includes(item)) {
        checkPass2 = true
      }
    })

    return checkPass1 || checkPass2
  }

  console.log("checkModelOrder contentJson.schedule: ", contentJson.schedule)

  // if (contentJson.schedule.length == 1) {
  //   console.log('modeling_nodelist:',modeling_nodeList.value[0].nodeInfo.label)
  //   moduleSchedule.push(modeling_nodeList.value[0].nodeInfo.label)  // 模块名称拼接的字符串
  //   algorithmSchedule.push(modeling_nodeList.value[0].nodeInfo.label_display)  // 算法名称拼接的字符串
  //   console.log('moduleSchedule: ', moduleSchedule)
  //   console.log('algorithmSchedule: ', algorithmSchedule)
  //   // 根据是否包含多传感器的算法，判断是否是针对多传感器的模型
  //   if (algorithmSchedule.indexOf("多传感器") != -1) {
  //     contentJson.multipleSensor = true  // 默认为false，即对单传感器数据的模型
  //   }
  // } else{
    //针对多个模块
  // 形成表示具体算法模块连接顺序的字符串
  for (let i = 0; i < contentJson.schedule.length; i++) {
    let module = contentJson.schedule[i]
    console.log("checkModelOrder module: ", module)
    let algorithmsS = modeling_nodeList.value.find(item => item.nodeInfo.label == module)
    console.log("algorithmsS: ", algorithmsS)
    algorithmSchedule.push(algorithmsS.nodeInfo.label_display)
    console.log("checkModelOrder algorithmsS: ", algorithmsS)
    moduleSchedule.push(module)
  }
  
  moduleStr = Object.values(moduleSchedule).join('')   // 所有模块的名称按顺序拼接起来的字符串
  algorithmStr = Object.values(algorithmSchedule).join('')  // 所有模块中的算法名称按顺序拼接起来的字符串
  console.log('moduleStr', moduleStr)
  console.log('algorithmStr', algorithmStr)
  // }
  if (modeling_nodeList.value.length) {
    // 首先判断模型中是否有数据源
    if (!moduleStr.match('数据源')) {
      ElMessage.error('模型中未包含数据源，请添加数据源模块')
      return false
    } else {
      if (modeling_nodeList.value.length == 1) {
        ElMessage.error('模型中仅包含数据源，无法运行，请添加其他模块')
        return false
      }
      if (moduleStr.indexOf('数据源') > 0) {
        ElMessage.error('数据源模块必须位于模型中第一个位置')
        return false
      }
    }
    moduleStr = moduleStr.replace('数据源', '')
    algorithmStr = algorithmStr.replace('数据源', '')
    console.log('moduleStr: ', moduleStr)
    console.log('algorithmStr: ', algorithmStr)
    // 首先判断模型中是否存在除了数据源之外的1个以上的模块，如果模型中只有一个模块，判断其是否可以独立地运行而不需要其他模块的支持
    if (modeling_nodeList.value.length == 2) {
      if (canRunSoloModule(moduleStr, algorithmStr)){
        // 如果模块可以单独运行，再进行模型中各个模块的参数设置的检查
        let checkParamsRight = checkModelParam()
        let isLofical_completeness = toObject().nodes.length-toObject().edges.length
        if (checkParamsRight && (isLofical_completeness==1)) {
          ElMessage({
            showClose: true,
            message: '模型正常，可以保存并运行',
            type: 'success'
          })
          modelCheckRight = true
          updateStatus('模型建立并已通过模型检查')
        } else {
          ElMessage({
            showClose: true,
            message: '请确保所有具有参数的模块的参数设置正确',
            type: 'warning'
          })
          return false
        }
      }else{

        let tip
        if (moduleStr.match('故障诊断')) {
          tip = '模型中包含故障诊断，建议在此之前进行特征提取和特征选择等操作'
        } else if (moduleStr.match('层次分析模糊综合评估')) {
          tip = '模型中包含层次分析模糊综合评估，建议在此之前进行特征提取和特征选择等操作'
        } else if (moduleStr.match('特征选择')) {
          tip = '模型中包含特征选择，建议在此之前进行特征提取等操作'
        } else if (moduleStr.match('故障预测')) {
          tip = '模型中包含故障预测，建议在此之前进行故障诊断'
        }

        ElMessage({
          message: '该算法无法单独使用，请结合相应的算法,' + tip,
          type: 'warning',
          showClose: true
        })

        return false
        // 无量纲化要检查是否使用模型训练师使用的标准化方法，对输入的原始信号无法使用模型训练时使用的标准化方法进行无量纲化
        if (moduleStr.match('无量纲化')) {
          let node
          for (let item of modeling_nodeList.value) {
            if (item.nodeInfo.label == '无量纲化') {
              node = item.nodeInfo
              break
            }
          }
          if (node?.parameters[node.use_algorithm]['useLog'] == true) {

            ElMessageBox.alert('如果要使用模型训练时使用的标准化方法进行无量纲化，请确保无量纲化模块之前对数据进行了特征提取，或者在参数设置中选择不使用模型训练时使用的标准化方法', '提示', {
              confirmButtonText: '确定',
              draggable: true,
              buttonSize: 'medium',
            })

            return false
          }
        }
        
      }
    } else {
      // 检查模型中是否存在未被连接的模块
      if (linkedList.length() != nodeList.value.length) {
        ElMessage({
          message: '请确保图中所有模块均已建立连接，且没有多余的模块',
          type: 'warning'
        })
        return false
      } else {
        // 模型正常连接的情况下进行模型逻辑以及模型参数的检查
        if (algorithmStr.match('多传感器') && algorithmStr.match('单传感器')) {
          ElMessage({
            showClose: true,
            message: '多传感器和单传感器的算法不能混合使用！',
            type: 'warning'
          })
          return false
        }
        if (moduleStr.match('故障诊断')) {
          // 如果是深度学习模型的故障诊断
          if (algorithmStr.match('深度学习模型的故障诊断') || algorithmStr.match('GRU的故障诊断') || algorithmStr.match('LSTM的故障诊断')) {
            if (moduleStr.indexOf('故障诊断') > 0) {
              // 检查深度学习模型的故障诊断之前是否包含不必要的模块
              let preModuleText = moduleStr.substring(0, moduleStr.indexOf('故障诊断'))
              if (preModuleText.match('特征提取') || preModuleText.match('特征选择') || preModuleText.match('无量纲化') || preModuleText.match('故障预测')) {
                ElMessage({
                  message: '深度学习模型的故障诊断不需要人工提取特征，因此其之前不需要包含如特征提取、特征选择等不必要的模块！',
                  type: 'warning',
                  showClose: true
                })
                return false
              }
            }
            // 如果使用深度学习模型的故障诊断之后有其他的模块
            if (moreText(moduleStr, '故障诊断')) {
              let nextModuleText = moduleStr.substring(moduleStr.indexOf('故障诊断'), moduleStr.length)  //故障诊断模块之后的其他模块名拼接的字符串
              if (nextModuleText.match('故障预测') || nextModuleText.match('层次分析模糊综合评估') || nextModuleText.match('层次朴素贝叶斯评估') || nextModuleText.match('层次逻辑回归评估')) {
                // 如果同时包含故障预测以及层次分析模糊综合评估
                let current: string
                if (nextModuleText.match('故障预测') && (nextModuleText.match('层次分析模糊综合评估') || nextModuleText.match('层次朴素贝叶斯评估') || nextModuleText.match('层次逻辑回归评估'))) {
                  // 获取健康评估模块所在的位置
                  let healthEvaluationIndex
                  if (nextModuleText.match('层次分析模糊综合评估')) {
                    healthEvaluationIndex = nextModuleText.indexOf('层次分析模糊综合评估')
                  } else if (nextModuleText.match('层次朴素贝叶斯评估')) {
                    healthEvaluationIndex = nextModuleText.indexOf('层次朴素贝叶斯评估')
                  } else {
                    healthEvaluationIndex = nextModuleText.indexOf('层次逻辑回归评估')
                  }
                  // 如果健康评估模块位置在深度学习的故障预测组件之后，需要进一步进行手工特征的提取
                  if (nextModuleText.indexOf('故障预测') > healthEvaluationIndex) {
                    ElMessage({
                      message: '注意故障预测应该在层次分析模糊综合评估之前运行',
                      type: 'warning',
                      showClose: true
                    })
                    return false
                  } else {
                    current = '故障预测'
                  }
                }

                // 因为之前的深度学习模型的故障诊断无法为故障预测或是健康评估提供样本特征，因此需要进行特征提取和特征选择
                if (nextModuleText.indexOf('故障预测') == -1) {
                  current = includeHealthEvaluation(moduleStr)
                  if (!current) {
                    message.error('模型检查出错，请重新链接模型')
                    return false
                  } 
                } else {
                  current = '故障预测'
                }
                let preModuleText = nextModuleText.substring(0, nextModuleText.indexOf(current))
                if (!preModuleText.match('特征提取特征选择') && !preModuleText.match('特征提取无量纲化特征选择') && !preModuleText.match('特征提取特征选择无量纲化')) {
                  ElMessage({
                    message: '建议在深度学习模型的故障诊断之后包含特征提取和特征选择模块',
                    type: 'warning',
                    showClose: true
                  })
                  return false
                }

              }
            }
          } else {
            // 如果是传统机器学习的故障诊断
            let preModuleText = moduleStr.substring(0, moduleStr.indexOf('故障诊断'))

            // 如果机器学习的故障诊断之前既不包含特征提取，也不包含特征选择
            if (!preModuleText.match('特征提取') && !preModuleText.match('特征选择')) {
              ElMessage({
                message: '建议在故障诊断之前进行特征提取和特征选择',
                type: 'warning',
                showClose: true
              })
              let preModule = linkedList.searchPre('故障诊断') // 寻找故障诊断之前的节点，即不符合规则的节点

              // 红色标明报错连线
              let sourceId = labelToId(preModule.value)
              let targetId = labelToId('故障诊断')

              plumbIns.select({source: sourceId, target: targetId}).setPaintStyle({
                stroke: '#E53935',
                strokeWidth: 7,
                outlineStroke: 'transparent',
                outlineWidth: 5,

              });
              return false
            } else {
              // 如果特征提取和特征选择同时存在
              if (preModuleText.match('特征提取') && preModuleText.match('特征选择')) {
                // 如果特征提取在特征选择之后，此时逻辑错误
                if (preModuleText.indexOf('特征提取') > preModuleText.indexOf('特征选择')) {
                  ElMessage({
                    message: '建议在特征提取之后进行特征选择',
                    type: 'warning',
                    showClose: true
                  })
                  return false
                }
              } else {
                // 如果只包含特征选择
                if (preModuleText.match('特征选择')) {
                  ElMessage({
                    message: '建议在特征提取之后再进行特征选择',
                    type: 'warning',
                    showClose: true
                  })
                  let preModule = linkedList.searchPre('特征选择') // 寻找特征选择之前的节点，即不符合规则的节点

                  // 红色标明报错连线
                  let sourceId = labelToId(preModule.value)
                  let targetId = labelToId('特征选择')

                  plumbIns.select({source: sourceId, target: targetId}).setPaintStyle({
                    stroke: '#E53935',
                    strokeWidth: 7,
                    outlineStroke: 'transparent',
                    outlineWidth: 5,

                  });
                  return false
                }
                // 如果只包含特征提取
                else if (preModuleText.match('特征提取')) {
                  ElMessage({
                    message: '因模型中包含机器学习的故障诊断，建议在特征提取之后进行特征选择',
                    type: 'warning',
                    showClose: true
                  })
                  let current = linkedList.search('特征提取') // 寻找特征选择之前的节点，即不符合规则的节点
                  let next = current.next
                  // 红色标明报错连线
                  let sourceId = labelToId(current.value)
                  let targetId = labelToId(next.value)

                  plumbIns.select({source: sourceId, target: targetId}).setPaintStyle({
                    stroke: '#E53935',
                    strokeWidth: 7,
                    outlineStroke: 'transparent',
                    outlineWidth: 5,

                  });
                  return false
                }

              }
            }
          }
        }

        if (moduleStr.match('特征提取故障诊断')) {
          let sourceId = labelToId('特征提取')
          let current = linkedList.search('特征提取')
          let next = current.next.value
          let targetId = labelToId(next)

          let connection = plumbIns.getConnections({source: sourceId, traget: targetId})
          console.log('connection: ', connection)

          plumbIns.select({source: sourceId, target: targetId}).setPaintStyle({
            stroke: '#E53935',
            strokeWidth: 7,
            outlineStroke: 'transparent',
            outlineWidth: 5,

          });
          ElMessage({
            showClose: true,
            message: '因模型中包含故障诊断，建议在特征提取之后包含特征选择',
            type: 'warning'
          })  
          return false
        }
        if (moduleStr.indexOf('小波变换') > 0) {
          // 小波变换只能针对信号序列，之前不能已经进行了特征提取
          let preModuleText = moduleStr.substring(0, moduleStr.indexOf('小波变换'))
          if (preModuleText.match('特征提取')) {
            ElMessage({
              showClose: true,
              message: '模型中对原始信号进行了特征提取，而小波变换只能针对信号序列',
              type: 'warning'
            })
            let preModule = linkedList.searchPre('小波变换') // 寻找健康评估之前的节点，即不符合规则的节点

            // 红色标明报错连线
            let sourceId = labelToId(preModule.value)
            let targetId = labelToId('小波变换')

            let connection = plumbIns.getConnections({source: sourceId, traget: targetId})
            console.log('connection: ', connection)

            plumbIns.select({source: sourceId, target: targetId}).setPaintStyle({
              stroke: '#E53935',
              strokeWidth: 7,
              outlineStroke: 'transparent',
              outlineWidth: 5,

            });
            return false
          }
        }
        if (includeHealthEvaluation(moduleStr)) {

          let healthEvaluation = includeHealthEvaluation(moduleStr)  //所包含的健康评估的组件名
          if (!moduleStr.match('特征提取')) {
            ElMessage({
              showClose: true,
              message: '因模型中包含层次分析模糊综合评估，建议在此之前包含特征提取',
              type: 'warning'
            })
            let current = linkedList.searchPre(healthEvaluation) // 寻找健康评估之前的节点，即不符合规则的节点

            // 红色标明报错连线
            let sourceId = labelToId(current.value)
            let targetId = labelToId(healthEvaluation)

            let connection = plumbIns.getConnections({source: sourceId, traget: targetId})
            console.log('connection: ', connection)

            plumbIns.select({source: sourceId, target: targetId}).setPaintStyle({
              stroke: '#E53935',
              strokeWidth: 7,
              outlineStroke: 'transparent',
              outlineWidth: 5,
            });
            return false
          }
          if (moreText(moduleStr, healthEvaluation)) {
            let sourceId = labelToId(healthEvaluation)
            let current = linkedList.search(healthEvaluation)
            let next = current.next.value
            let targetId = labelToId(next)

            plumbIns.select({source: sourceId, target: targetId}).setPaintStyle({
              stroke: '#E53935',
              strokeWidth: 7,
              outlineStroke: 'transparent',
              outlineWidth: 5,

            });
            ElMessage({
              showClose: true,
              message: '注意健康评估之后无法连接更多的模块',
              type: 'warning'
            })
            return false
          }

        }
        if (moduleStr.match('特征选择')) {
          let preModuleText = moduleStr.substring(0, moduleStr.indexOf('特征选择'))
          if (!preModuleText.match('特征提取')) {
            ElMessage({
              showClose: true,
              message: '因模型中包含特征选择，建议在此之前包含特征提取',
              type: 'warning'
            })
            let preModule = linkedList.searchPre('特征选择')
            let sourceId = labelToId(preModule)
            let targetId = labelToId('特征选择')

            // 通过jsPlumb实例对象的select方法选择连线，并设置连线的样式
            plumbIns.select({source: sourceId, target: targetId}).setPaintStyle({
              stroke: '#E53935',
              strokeWidth: 7,
              outlineStroke: 'transparent',
              outlineWidth: 5,

            });

            return false
          }
        }
        if (algorithmStr.match('深度学习模型的故障诊断') || algorithmStr.match('GRU的故障诊断') || algorithmStr.match('LSTM的故障诊断')) {
          // 如果使用深度学习的故障诊断之前有其他模块，则要进行限定

          if (moduleStr.indexOf('故障诊断') != 0) {
            let preText = moduleStr.substring(0, moduleStr.indexOf('故障诊断'))
            // 检查使用深度学习的故障诊断之前是否有特征提取等不合理的模块
            if (preText.match('特征提取') || preText.match('特征选择') || preText.match('无量纲化')) {
              ElMessage({
                showClose: true,
                message: '使用深度学习模型的故障诊断不需要进行特征提取或是特征选择，请删除相关模块！',
                type: 'warning'
              })
              return false
            }

          }
        }
        if (algorithmStr.match('多传感器') && algorithmStr.match('单传感器')) {
          ElMessage({
            showClose: true,
            message: '针对单传感器的算法无法与针对多传感器的算法共用',
            type: 'warning'
          })
          return false
        }
        if (moduleStr.match('无量纲化')) {
          let node
          for (let item of modeling_nodeList.value) {
            if (item.nodeInfo.label.match('无量纲化')) {
              node = item.nodeInfo
              break
            }
          }
          let useLog = node.parameters[node.use_algorithm]['useLog']  // 获取无量纲化模块的参数
          // 无量纲化处理前没有其他模块
          if (moduleStr.indexOf('无量纲化') == 0) {
            // 检查无量纲化参数设置是否合理
            if (useLog == true) {

              ElMessageBox.alert('如果要使用模型训练时使用的标准化方法进行无量纲化，请确保无量纲化模块之前对数据进行了特征提取，或者在参数设置中选择不使用模型训练时使用的标准化方法', '提示', {
                confirmButtonText: '确定',
                draggable: true,
                buttonSize: 'medium',
              })
              return false
            }
          } else {

            // 检查无量纲化处理前的其他模块是否符合无量纲化的运行规则
            let preModule = moduleStr.substring(0, moduleStr.indexOf('无量纲化'))
            if (preModule.match('特征提取') && useLog == false) {
              ElMessageBox.alert(
                  '因为无量纲化模块之前已经进行了特征提取，请在无量纲化的参数设置中选择使用模型训练时使用的标准化方法进行无量纲化',
                  '提示',
                  {
                    confirmButtonText: '确定',
                    draggable: true,
                    buttonSize: 'medium',
                  }
              )
              return false
            } else if (!preModule.match('特征提取') && useLog == true) {
              ElMessageBox.alert(
                  '无量纲化模块之前未进行特征提取，因此无法使用模型训练时使用的标准化方法进行无量纲化，请在无量纲化的参数设置中选择不使用模型训练时使用的标准化方法进行无量纲化',
                  '提示',
                  {
                    confirmButtonText: '确定',
                    draggable: true,
                    buttonSize: 'medium',
                  }
              )
            }
          }

        }

        // 检查模型中是否使用了深度学习模型的故障诊断
        const useDeepLearningModule = (algorithmStr: string) => {
          return algorithmStr.match('LSTM的故障诊断') || algorithmStr.match('GRU的故障诊断') || algorithmStr.match('一维卷积深度学习模型的故障诊断') || algorithmStr.match('时频图深度学习模型的故障诊断')
        }
        // 规定插值处理只能是在模型中的开始位置
        if (moduleStr.match('插值处理')) {
          if (moduleStr.indexOf('插值处理') != 0) {
            ElMessage({
              showClose: true,
              message: '插值处理只能处在模型中的开始位置',
              type: 'warning'
            })
            let preModule = linkedList.searchPre('插值处理')
            let sourceId = labelToId(preModule)
            let targetId = labelToId('插值处理')

            // 通过jsPlumb实例对象的select方法选择连线，并设置连线的样式
            plumbIns.select({source: sourceId, target: targetId}).setPaintStyle({
              stroke: '#E53935',
              strokeWidth: 7,
              outlineStroke: 'transparent',
              outlineWidth: 5,

            });
            return false
          }
        }
        if (moduleStr.match('故障预测')) {
          // 故障预测之前必须进行故障诊断
          if (moduleStr.indexOf('故障预测') <= 0) {
            ElMessage({
              showClose: true,
              message: '故障预测之前需要进行故障预测',
              type: 'warning'
            })

            return false
          } else {
            let preModuleText = moduleStr.substring(0, moduleStr.indexOf('故障预测'))
            if (!preModuleText.match('故障诊断')) {
              ElMessage({
                showClose: true,
                message: '故障预测之前需要进行故障诊断',
                type: 'warning'
              })
              // 将报错的连线标注为红色

              let preModule = linkedList.searchPre('故障预测')
              let sourceId = labelToId(preModule.value)
              let targetId = labelToId('故障预测')

              // 通过jsPlumb实例对象的select方法选择连线，并设置连线的样式0
              plumbIns.select({source: sourceId, target: targetId}).setPaintStyle({
                stroke: '#E53935',
                strokeWidth: 7,
                outlineStroke: 'transparent',
                outlineWidth: 5,

              });
              return false
            }

          }
        }
        if (moduleStr.match('故障诊断')) {
          let useDeepLearning = useDeepLearningModule(algorithmStr)
          if (moreText(moduleStr, '故障诊断')) {
            // 机器学习的故障诊断之后只能是进行故障预测或是健康评估

            if (!useDeepLearning && !checkSubstrings(moduleStr, '故障诊断', ['层次分析模糊综合评估', '故障预测', '层次朴素贝叶斯评估', '层次逻辑回归评估', '健康评估'])) {
              ElMessage({
                showClose: true,
                message: '注意故障诊断之后仅能进行故障预测或是健康评估！',
                type: 'warning'
              })
              // 将报错的连线标注为红色
              let sourceId = labelToId('故障诊断')
              let current = linkedList.search('故障诊断')
              let next = current.next.value       // 寻找目标连线的源节点和目标节点
              let targetId = labelToId(next)

              // 通过jsPlumb实例对象的select方法选择连线，并设置连线的样式
              plumbIns.select({source: sourceId, target: targetId}).setPaintStyle({
                stroke: '#E53935',
                strokeWidth: 7,
                outlineStroke: 'transparent',
                outlineWidth: 5,

              });

              return false
            }
          }
          // 如果模型中包含SVM的故障诊断，则需要先加入无量纲化操作
          if (algorithmStr.match('SVM的故障诊断')) {
            if (!moduleStr.match('无量纲化') || !checkSubstrings(moduleStr, '无量纲化', ['故障诊断'])) {
              ElMessage({
                showClose: true,
                message: '因模型中包含SVM的故障诊断，需要在此之前加入z-score标准化操作',
                type: 'warning'
              })
              // 将报错的连线标注为红色
              let sourceId = labelToId('特征选择')
              let current = linkedList.search('特征选择')
              let next = current.next.value       // 寻找目标连线的源节点和目标节点
              let targetId = labelToId(next)

              // 通过jsPlumb实例对象的select方法选择连线，并设置连线的样式
              plumbIns.select({source: sourceId, target: targetId}).setPaintStyle({
                stroke: '#E53935',
                strokeWidth: 7,
                outlineStroke: 'transparent',
                outlineWidth: 5,

              });
              return false
            } else {
              if (!algorithmStr.match('z-score标准化')) {
                ElMessage({
                  showClose: true,
                  message: '因模型中包含SVM的故障诊断，需要在此之前加入z-score标准化操作',
                  type: 'warning'
                })
                return false
              }
            }

          }
        }
        // 进行模型参数设置的检查
        let isLofical_completeness = toObject().nodes.length-toObject().edges.length
        let checkParamsRight = checkModelParam()
        if (checkParamsRight && (isLofical_completeness==1)) {
          ElMessage({
            showClose: true,
            message: '模型正常，可以保存并运行',
            type: 'success'
          })
          modelCheckRight = true
          updateStatus('模型建立并已通过模型检查')
        } else {
          ElMessage({
            showClose: true,
            message: '请确保所有具有参数的模块的参数设置正确',
            type: 'warning'
          })
          return false
        }
      }
    }
  } else {
    ElMessage({
      message: '请先建立模型',
      type: 'warning'
    })
    return false
  }
  return true
};

// 标记模型已经通过检查
const modelHasBeenChecked = ref(false)
//检查模型
function checkModelOfViewFlow() {
  let checkContent = false
  let checkOrder = false
  //检查时构建contentJson
  if(modeling_nodeList.value.length > 1){
    checkContent = buildContentJson()
  }else{
    ElMessage({
      message: '请先建立包含数据源与至少一个组件的模型',
      type: 'warning'
    })
    return false
  }

  console.log("检查模型时构建contentJson: ", contentJson)
  // 进行模型参数设置和逻辑的检查
  checkOrder = checkModelOrder()

  if (checkContent && checkOrder){
    modelHasBeenChecked.value = true
    // disabledStateOfControlBtn.value.saveModelOfViewFlowBtn = false
    // disabledStateOfControlBtn.value.runModelOfViewFlowBtn = false
  }
  // console.log("check_order_right: ", buildContentJson())
}

//构建处理顺序
// 构建邻接表和入度表
const adjacencyList = ref([]);
const inDegree = ref({});
// 排序
// 初始化顺序数组和已访问节点集合
let order = ref([]);
const visited = ref(new Set());

// 函数用于递归地构建顺序
function buildOrder(nodeId) {
  if (!order.value.length) {
    console.log("添加节点头", nodeId)
    order.value.push(nodeId)
  }
  // 查找下一条边（从当前节点出发的边）
  const nextNodes = toObject().edges.find(edge => edge.source == nodeId)?.target;
  //找到下一条边
  const nextNodes1 = toObject().edges.find(edge => edge.source == nodeId)
  console.log('增值组件的构建',nextNodes1)
  if (!nextNodes) {
    return
  }
  // 将找到的边添加到顺序数组
  order.value.push(nextNodes);
  console.log("添加节点1", nextNodes)
  // 递归地构建顺序
  buildOrder(nextNodes)
}

//构建contentJson
function buildContentJson() {
  //初始化邻接表和入度表
  adjacencyList.value = [];
  inDegree.value = {};
  // 排序
  // 初始化顺序数组和已访问节点集合
  order.value = [];
  visited.value = new Set();
  // 执行拓扑排序并获取节点的处理顺序
  console.log("构建处理逻辑: ")
  let isLofical_completeness = toObject().nodes.length-toObject().edges.length
  if(isLofical_completeness != 1){
    console.log("构建处理逻辑: ", toObject().edges)
   return true
  }else{
    toObject().edges.forEach(edge => {
      console.log("edge: ", edge)
      const {source, target} = edge;
      // 添加节点到节点数组，如果它还不在数组中
      if (!adjacencyList.value.includes(source)) {
        adjacencyList.value.push(source);
      }
      if (!adjacencyList.value.includes(target)) {
        adjacencyList.value.push(target);
      }
      if (!inDegree[target]) {
        inDegree[target] = 1;
      }
    });
    console.log("邻接表: ", inDegree)
    console.log("邻接表节点: ", adjacencyList)
    // 找到起始节点
    // 使用 filter() 方法移除在adjacencyList中作为键的键
    const filteredKeys = adjacencyList.value.filter(key => !(key in inDegree));
    console.log('头节点：', filteredKeys);
// 从第一个节点开始构建顺序
//   const startNode = filteredKeys; // 假设第一个边的 source 是起始节点
    buildOrder(filteredKeys[0]);
    console.log('构建的顺序：', order); // 输出构建的顺序
    jsonClear()
    for (let i = 0; i < modeling_nodeList.value.length; i++) {
      let dict = modeling_nodeList.value[i]
      console.log('保存的dict.use_algorithm: ', dict.nodeInfo.use_algorithm)
      if (!dict.nodeInfo.use_algorithm) {
        ElMessage({
          message: '请设置每个算法的必选属性',
          type: 'error'
        })
        return false
      }

      contentJson.algorithms[dict.nodeInfo.label] = dict.nodeInfo.use_algorithm
      console.log("contentJson: ", contentJson)
      if (!contentJson.modules.includes(dict.nodeInfo.label) && dict.nodeInfo.id !== '4') {
        contentJson.modules.push(dict.nodeInfo.label);
      }

      // 选择特征提取需要提取的参数
      if (dict.nodeInfo.id == '1.2') {
        let params: Object = dict.nodeInfo.parameters[dict.nodeInfo.use_algorithm]
        if (!features.value.length) {
          ElMessage({
            message: '请设置每个算法的必选属性',
            type: 'error'
          })
          return false
        }
        console.log('features: ', features.value)
        for(let key of Object.keys(params)){
          params[key] = false
        }
        features.value.forEach(element => {
          if (params[element] == false) {
            console.log(' element设为真',element)
            params[element] = true
          }
        });
        contentJson.parameters[dict.nodeInfo.use_algorithm] = params
        continue
      }
      contentJson.parameters[dict.nodeInfo.use_algorithm] = dict.nodeInfo.parameters[dict.nodeInfo.use_algorithm]

    }

    contentJson.schedule.length = 0
// 建立处理顺序
    console.log('新模型顺序: ', order)
    //将顺序转化成中文名称
    const lettersOnly = order.value.map(item => {
      //处理单个字符串
      return item.replace(/[^a-zA-Z_\u4e00-\u9fa5]/g, '')
    }).filter(item => item.length > 0); // 过滤掉空字符串
    console.log('新模型顺序22222: ', lettersOnly)

    for (let i = 0; i < lettersOnly.length; i++) {
      let obj = Object.keys(contentJson.algorithms).find(key => contentJson.algorithms[key] === lettersOnly[i])
      contentJson.schedule.push(obj)
    }
    console.log('构建的contentJson', contentJson);
  }
  return true
}



interface Tree {
  label: string; // 节点名称
  value: string; // 节点id
  disabled: boolean; // 是否禁用添加子类型
  children?: Tree[]; // 子节点
}
const dataSourceOfTree = reactive<Tree[]>([])

// 获取模型结构树
const getComponentTrees = async() => {
  api.get("user/get_component_trees").then((response: any) => {
    // 请求成功，后端返回数据
    if (response.data.code === 200) {
      dataSourceOfTree.length = 0;
      response.data.trees.map((tree: Tree) => dataSourceOfTree.push(tree));
      console.log("获取到树形结构: ", dataSourceOfTree);
    } else {
      ElMessage.error("获取树形结构失败，" + response.data.message);
    }
  });
};

//保存模型，从模型结构树中选择一个类型
async function saveModelOfViewFlow() {
  if (!modelHasBeenChecked.value){
    ElMessage.warning("请先点击检查按钮，完成模型检查")
    return
  }
  //显示保存模型表单
  await getComponentTrees();
  console.log("saveModelOfViewFlow trees: ", dataSourceOfTree)
  dialogModle.value = true
}

//运行模型
function runModelOfViewFlow() {

  if (!modelHasBeenChecked.value){
    ElMessage.warning("请先点击检查按钮，完成模型检查")
    return
  }

  if (!usingDatafile.value) {
    ElMessage({
      message: '请先加载数据',
      type: 'warning'
    })
    return
  }
  console.log("runModelOfViewFlow modelLoaded: ", modelLoaded.value)
  const data = new FormData()
  data.append("file_name", usingDatafile.value)  // 所使用的数据文件
  data.append('params', JSON.stringify(contentJson))  // 模型信息
  // console.log('params: ', contentJson)
  if (usingDatafile.value == '无') {
    ElMessage({
      message: '当前加载的数据为空，请先加载数据文件',
      type: 'error'
    })
    return
  }
  ElNotification.info({
    title: 'Waiting',
    message: '正在运行，请等待...'
  })
  canShutdown.value = false

  percentage.value = 0; // 重置进度条

  fastTimerId = setInterval(() => {
    if (percentage.value < 50) {
      percentage.value += 10;
    } else {
      // 达到50%时，清除快速定时器并启动慢速定时器
      clearInterval(fastTimerId);
      slowTimerId = setInterval(() => {
        if (percentage.value < 90) {
          percentage.value += 10;
        } else {
          // 达到100%时清除慢速定时器
          clearInterval(slowTimerId);
        }
      }, 3000);
    }
  }, 1000);

  // 显示进度条
  resultsViewClear()
  processing.value = true
  showStatusMessage.value = false
  showPlainIntroduction.value = false

  api.post('user/run_with_datafile_on_cloud/', data,
      {
        headers: {"Content-Type": 'multipart/form-data'},
        cancelToken: source.token, // 将cancelToken传递给axios
      }
  ).then((response) => {
    if (response.data.code == 401) {
      ElMessageBox.alert('登录状态已失效，请重新登陆', '提示', {
        confirmButtonText: '确定',
        callback: (action: Action) => {
          router.push('/')
        },
      })
    }
    if (response.data.code === 200) {

      if (!processIsShutdown.value) {
        ElNotification.success({
          title: 'Success',
          message: '程序运行完成',
        })
        responseResults = response.data.results
        missionComplete.value = true
        statusMessageToShow.value = statusMessage.success
        showResultOfElMain()
      } else {
        processIsShutdown.value = false
      }
    } else if (response.data.code == 404) {
      statusMessageToShow.value = statusMessage.error
      ElMessage({
        message: response.data.message,
        type: 'warning'
      })
    }
    clearInterval(fastTimerId);
    clearInterval(slowTimerId);
    setTimeout(function () {
      processing.value = false
    }, 700)
    percentage.value = 100;
    canShutdown.value = true

    resultsViewClear()

    showStatusMessage.value = true
    showPlainIntroduction.value = false
  })
      .catch(error => {

        if (error.response) {
          // 请求已发出，服务器响应了状态码，但不在2xx范围内
          console.log(error.response.status); // HTTP状态码
          console.log(error.response.statusText); // 状态消息

        } else if (error.request) {
          // 请求已发起，但没有收到响应
          console.log(error.request);
        } else {
          // 设置请求时触发了错误
          console.error('Error', error.message);
        }

        ElNotification.error({
          title: 'Error',
          message: '运行出错，' + error.response.data?.message,
        })
        loading.value = false
        processing.value = false

        canShutdown.value = true
        statusMessageToShow.value = statusMessage.error
        resultsViewClear()
        showStatusMessage.value = true
        missionComplete.value = false

      })
}

//终止运行
function stopRunningModelOfViewFlow() {

}

//配置模型
function setModelConfigRunningModelOfViewFlow() {
}

//实现自动垂直水平布局功能、打乱功能
import {useRunProcess} from './vueflow/useRunProcess'
import {useShuffle} from './vueflow/useShuffle'
import {useLayout} from './vueflow/useLayout'
import CustomForm from "@/components/vueflow/CustomForm.vue";
import { get, result } from 'lodash';

const cancelOnError = ref(true)
const shuffle = useShuffle()
const {graph, layout, previousDirection} = useLayout()
const {run, stop, reset, isRunning} = useRunProcess({graph, cancelOnError})
const {fitView} = useVueFlow()

async function shuffleGraph() {
  if (modeling_nodeList && modeling_nodeList.value.length > 0) {
    await stop()
    reset(modeling_nodeList.value)
    modeling_edgesList.value = shuffle(modeling_nodeList.value)
    nextTick(() => {
      layoutGraph(previousDirection.value)
    })
    closeResultOfElMain()
  }
}

async function layoutGraph(direction) {
  if (modeling_nodeList && modeling_nodeList.value.length > 0) {
    await stop()
    reset(modeling_nodeList.value)
    modeling_nodeList.value = layout(modeling_nodeList.value, modeling_edgesList.value, direction)
    nextTick(() => {
      fitView()
    })
    closeResultOfElMain()
  }
}

const transfer = ref({
  '特征提取': '',
  '无量纲化': '',
  '特征选择': '',
  '小波变换': '',
})
//配置菜单模块start
const isHiddenConfigPanelOfNode = ref(false)
//包含那些菜单(添加的是：拖拽组件nodeInfo.id)
const containsMenuSettings = ref([])
//监控（浅监控，只是观察添加和删除的变化）的modeling_nodeList变化
watch(modeling_nodeList, (newVal, oldVal) => {
  const addedItems = newVal.filter(item => !oldVal.includes(item));
  if (addedItems.length) {
    modelHasBeenChecked.value = false
    missionComplete.value = false
    
    updateStatus("请建立模型并点击检查模型")
    console.log('添加的元素:', addedItems);
    console.log("添加元素后的modeling_nodeList: ", modeling_nodeList)
    parameter_dict.value = {}
    console.log("监听器添加元素后parameter_dict: ", parameter_dict.value)
    console.log("动态修改数据: ",item.use_algorithm)
    missionComplete.value = false
    // disabledStateOfControlBtn.value.saveModelOfViewFlowBtn = true
    // disabledStateOfControlBtn.value.runModelOfViewFlowBtn = true
    if(item.nodeId=='1.2'){
      console.log("进入1.2",)
         transfer.value['特征提取'] = item.use_algorithm
    }
    if(item.nodeId=='1.3'){
      transfer.value['特征选择'] = item.use_algorithm
    }
    if(item.nodeId=='1.4'){
      transfer.value['小波变换'] = item.use_algorithm
    }
    if(item.nodeId=='1.5'){
      transfer.value['无量纲化'] = item.use_algorithm
    }
    console.log("监听器添加元素后transfer: ", transfer.value)
    modeling_nodeList.value.forEach((items,index) => {
        parameter_dict.value[items.nodeInfo.use_algorithm] = index
    })

    addedItems.forEach(item => {
      containsMenuSettings.value.push(item.nodeInfo.id);

    })
    
  } else {
    const removedItems = oldVal.filter(item => !newVal.includes(item));
    if (removedItems.length) {
      missionComplete.value = false
      modelHasBeenChecked.value = false
      if(modeling_nodeList.value.length>0){
        updateStatus("请建立模型并点击检查模型")
      }else{
        updateStatus("未建立模型")
      }
      // updateStatus("请建立模型并点击检查模型")
      // disabledStateOfControlBtn.value.saveModelOfViewFlowBtn = true
      // disabledStateOfControlBtn.value.runModelOfViewFlowBtn = true
      console.log('删除的元素:', removedItems);
      parameter_dict.value = {}
      console.log("parameter_dict.value: ", parameter_dict.value)
      modeling_nodeList.value.forEach((items,index) => {
        parameter_dict.value[items.nodeInfo.use_algorithm] = index
      })
      console.log("监听器删除元素后parameter_dict: ", parameter_dict)
      removedItems.forEach(item => {
        let id = containsMenuSettings.value.indexOf(item.nodeInfo.id)
        if (id != -1) {
          containsMenuSettings.value.splice(id, 1)
        }
      })
    }
  }
  console.log("containsMenuSettings: ", containsMenuSettings)
}, {deep: false});

//打开配置菜单
function openConfigPanelOfModelNode() {
  console.log("是否绑定: ", modeling_nodeList.value)
  if (isHiddenConfigPanelOfNode.value) {
    isHiddenConfigPanelOfNode.value = false;
  }
}


// 监听边的变化
watch(modeling_edgesList, (newVal, oldVal) => {
  const addedItems = newVal.filter(item => !oldVal.includes(item));
  console.log("监听器添加元素后newVal: ", newVal)
  if (addedItems.length) {
    modelHasBeenChecked.value = false
    missionComplete.value = false

    console.log('添加的元素:', addedItems);
    console.log("添加元素后的modeling_edgesList: ", modeling_edgesList)
    parameter_dict.value = {}
    // console.log("监听器添加元素后parameter_dict: ", .value.value)
    console.log("动态修改数据: ",item.use_algorithm)
    missionComplete.value = false
    // disabledStateOfControlBtn.value.saveModelOfViewFlowBtn = true
    // disabledStateOfControlBtn.value.runModelOfViewFlowBtn = true
    // if(item.nodeId=='1.2'){
    //   console.log("进入1.2",)
    //      transfer.value['特征提取'] = item.use_algorithm
    // }
    // if(item.nodeId=='1.3'){
    //   transfer.value['特征选择'] = item.use_algorithm
    // }
    // if(item.nodeId=='1.4'){
    //   transfer.value['小波变换'] = item.use_algorithm
    // }
    // if(item.nodeId=='1.5'){
    //   transfer.value['无量纲化'] = item.use_algorithm
    // }
    // console.log("监听器添加元素后transfer: ", transfer.value)
    // modeling_nodeList.value.forEach((items,index) => {
    //     parameter_dict.value[items.nodeInfo.use_algorithm] = index
    // })

    // addedItems.forEach(item => {
    //   containsMenuSettings.value.push(item.nodeInfo.id);

    // })
    
  } else {
    const removedItems = oldVal.filter(item => !newVal.includes(item));
    if (removedItems.length) {
      missionComplete.value = false
      modelHasBeenChecked.value = false
      // disabledStateOfControlBtn.value.saveModelOfViewFlowBtn = true
      // disabledStateOfControlBtn.value.runModelOfViewFlowBtn = true
      console.log('删除的元素:', removedItems);
      parameter_dict.value = {}
      console.log("parameter_dict.value: ", parameter_dict.value)
      // modeling_nodeList.value.forEach((items,index) => {
      //   parameter_dict.value[items.nodeInfo.use_algorithm] = index
      // })
      console.log("监听器删除元素后parameter_dict: ", parameter_dict)
      // removedItems.forEach(item => {
      //   let id = containsMenuSettings.value.indexOf(item.nodeInfo.id)
      //   if (id != -1) {
      //     containsMenuSettings.value.splice(id, 1)
      //   }
      // })
    }
  }
  // console.log("containsMenuSettings: ", containsMenuSettings)
}, {deep: false});


//关闭配置菜单
function closeConfigPanelOfModelNode() {
  if (!isHiddenConfigPanelOfNode.value) {
    isHiddenConfigPanelOfNode.value = true;
  }
}

//配置菜单控制面板激活
const activeNamesOfConfigPanelOfModelNode = ref([])

function onItemClickOfConfigPanelOfModelNode(data) {

}

//配置菜单模块end

///////////////////////////////////////////////////////////////////////////////建模区end
///////////////////////////////////////////////////////////////////////////////以下还是原来的
// 删除增值服务组件时需要刷新增值组件列表
const handleDeleteExtraModule = () => {
  getExtraAlgorithmMao();
}
// 上传增值服务组件时需要刷新增值组件列表
const handleAddExtraModule = () => {
  getExtraAlgorithmMao();
}

//控制增值组件目录开关
const isShowSecondButton = ref(false);
const fetchedExtraAlgorithmList = ref([])

//构造数据
const options_modules = ref([
  {
    label: '插值处理', id: '1.1', use_algorithm: null, alias: null, machineLearning: '', parameters: {
      'private_interpolation': '',
    }, tip_show: false, tip: '使用专有插值处理方法', optional: false
  },
  {
    label: '特征提取', id: '1.2', use_algorithm: null, alias: null, machineLearning: '', parameters: {
      'private_feature_extraction': '',
    }
  },
  {
    label: '无量纲化', id: '1.5', use_algorithm: null, alias: null, machineLearning: '', parameters: {
      'private_scaler': {useLog: false, algorithm: ''}
    }, tip_show: false, tip: '使用专有无量纲化处理方法', optional: true
  },
  {
    label: '特征选择', id: '1.3', use_algorithm: null, alias: null, machineLearning: '', parameters: {
      'extra_feature_selection': {rule: 1, threshold1: 0.1, threshold2: 0.1}
    }, tip_show: false, tip: '使用专有特征选择方法', optional: true
  },
  {
    label: '小波变换', id: '1.4', use_algorithm: null, alias: null, machineLearning: '', parameters: {
      'extra_wavelet_transform': ''
    }, tip_show: false, tip: '对输入信号进行小波变换', optional: true
  },
  {
    label: '故障诊断', id: '2.1', use_algorithm: null, alias: null, machineLearning: '', parameters: {
      'private_fault_diagnosis_machine_learning': '',
      'private_fault_diagnosis_deeplearning': '',
    }, tip_show: false, tip: '使用专有故障诊断方法', optional: false
  },
  {
    label: '故障预测', id: '2.2', use_algorithm: null, alias: null, machineLearning: '', parameters: {

      'private_fault_prediction': {}
    }, tip_show: false, tip: '使用专有故障预测方法', optional: false
  },
  {
    label: '专有健康评估', id: '3.4', use_algorithm: null, alias: null, machineLearning: '', parameters: {
      'extra_health_evaluation': ''
    }, tip_show: false, tip: '使用专有健康评估的评价方法', optional: false,
  },

])

//构造增值组件菜单,复制速度不能过快，foreach和map太快会直接覆盖到前面的内容
function updateOptionsWithBackendData(data) {
  // 清空 fetchedExtraAlgorithmList，准备存储新数据
  fetchedExtraAlgorithmList.value = [];

  // 使用 for 循环遍历 data 数组
  for (let i = 0; i < data.length; i++) {
    const item = data[i];
    // 在 options_modules 中查找与当前 item 的 algorithmType 匹配的选项
    const foundOption = options_modules.value.find(option => option.label === item.algorithmType);

    // 如果找到了匹配的选项
    if (foundOption) {
      // 创建一个新对象，它是 foundOption 的副本
      const newOption = {...foundOption};

      // 更新新对象的属性
      newOption.label = item.algorithmType
      // newOption.use_algorithm = item.algorithmName;
      // newOption.use_algorithm = newOption.parameters[]
      newOption.alias = item.alias;
      newOption.machineLearning = item.machineLearning;

      // 将新对象添加到 fetchedExtraAlgorithmList 中
      fetchedExtraAlgorithmList.value.push(newOption);
    }
  }

}

//获取用户的增值组件列表
const getExtraAlgorithmMao = () => {
  api.get("/user/user_fetch_extra_algorithm/").then((response: any) => {
    if (response.data.code == 401) {
      ElMessageBox.alert("登录状态失效，请重新登陆", "提示", {
        confirmButtonText: "确定",
        callback: () => {
          router.push("/");
        },
      });
    }
    if (response.data.code == 200) {
      console.log('信息：', response.data.data)
      updateOptionsWithBackendData(response.data.data)
    }
  });
};

//处理增值组件的拖拽
const handleDragendAdd = (ev, algorithm, node) => {
  // 使用find方法查找具有特定alias的对象
  console.log("现拖拽algorithm", algorithm)
  const foundObject = fetchedExtraAlgorithmList.value.find(obj => obj.alias === algorithm)
  const parametersKey = Object.keys(foundObject.parameters)[0]
  // 如果找到了对象，复制其parameters的键
  if (foundObject) {
    console.log("找到的算法文件", parametersKey); // 输出: ['private_fault_diagnosis_deeplearning', 'private_fault_diagnosis_machine_learning']
  }
  node.parameters[parametersKey] = node.alias
  console.log("node.parameters", node.parameters)
  // 拖拽进来相对于地址栏偏移量
  const evClientX = ev.clientX
  const evClientY = ev.clientY
  let left
  if (evClientX < 300) {
    left = evClientX + 'px'
  } else {
    left = evClientX - 300 + 'px'
  }

  let top = 50 + 'px'
  const nodeId = node.id
  const nodeInfo = {
    label_display: node.alias,   // 具体算法的名称

    label: node.label,      // 算法模块名称
    id: node.id,
    nodeId,
    nodeContainerStyle: {
      left: left,
      top: top,
    },
    use_algorithm: parametersKey,
    parameters: node.parameters,
    optional: node.optional
  }

  console.log(nodeInfo)
  // 针对时域或是频域特征给出不同的可选特征

  // console.log(nodeInfo)
  //算法模块不允许重复
  if (nodeList.value.length === 0) {
    nodeList.value.push(nodeInfo)
  } else {
    let isDuplicate = false;
    for (let i = 0; i < nodeList.value.length; i++) {
      let nod = nodeList.value[i];
      if (nod.id == node.id) {
        // window.alert('不允许出现重复模块');
        ElMessage({
          message: '不允许出现同一类别的算法',
          type: 'warning'
        })
        isDuplicate = true;
        break;
      }
    }
    // 向节点列表中添加新拖拽入可视化建模区中的模块
    if (!isDuplicate) {
      nodeList.value.push(nodeInfo);
      console.log('画布列表', nodeList.value)
    }

  }

  // 将节点初始化为可以连线的状态
  nextTick(() => {
    plumbIns.draggable(nodeId, {containment: "efContainer"})

    if (node.id < 4) {
      plumbIns.makeSource(nodeId, deff.jsplumbSourceOptions)
    }

    if (node.id == '4') {
      plumbIns.makeSource(nodeId, deff.jsplumbSourceOptions)
      return
    }

    plumbIns.makeTarget(nodeId, deff.jsplumbTargetOptions)

  })
}

// 动态绑定选择基础组件和系统模型按钮的样式，使得其背景色动态改变
const getRadioButtonStyle = (value) => {
  const baseStyle = {
    width: '100%',
    border: 'none',
    borderRadius: 0,
    fontWeight: 'bolder',
    fontSize: '22px'
  };

  if (modelSelection.value === value) {
    return {
      ...baseStyle,
      color: 'white',
      'background-color': "#4fb0ff"
    };
  } else {
    return {
      ...baseStyle,
      color: '#558b48'
    };
  }
}

// 建模区中各个算法节点的图标url
const setIconOfAlgorithms = (label: string) => {

  let iconName;
  switch (label) {
    case '插值处理':
      iconName = 'interpolation-icon.svg'
      break
    case '特征提取':
      iconName = 'extraction-icon.svg'
      break
    case '无量纲化':
      iconName = 'normalization-icon.svg'
      break
    case '特征选择':
      iconName = 'feature-selection-icon.svg'
      break
    case '小波变换':
      iconName = 'wavelet-icon.svg'
      break
    case '数据源':
      iconName = 'data-source-icon.svg'
      break
    case '故障诊断':
      iconName = 'fault-diagnosis-icon.svg'
      break
    case '故障预测':
      iconName = 'fault-prediction-icon.svg'
      break
    case '自定义模块':
      iconName = 'custom-module-icon.svg'
      break
    case '层次分析模糊综合评估':
    case '层次逻辑回归评估':
    case '层次朴素贝叶斯评估':
    case '健康评估':
      iconName = 'health-evaluation-icon.svg'
  }
  return new URL(`../assets/${iconName}`, import.meta.url).href
}

// 关于如何自定义建模的介绍
// const showHowToCustomizeModel = ref(true);
const howToCustomizeModel = "### 如何自定义建模？ \n " +
    "#### 1. 点击左侧菜单栏中的“基础组件”，在基础组件菜单下，可以选择任意组件拖入建模区, 右键点击建模区中的节点可进行相关参数配置。 \n" +
    "#### 2. 通过建模区中算法节点的附着点可进行算法模块间的连接 \n" +
    "#### 3. 建立模型时，还需包括数据源组件，将左侧的数据源组件拖入建模区，连接至模型的开始处，并且右键点击数据源组件可以进行数据的上传和加载操作。 \n" +
    "### 推荐的模型流程 \n"
// "#### 1. 机器学习的故障诊断 \n " +
// "<img src='./src/assets/customize-model-1.png' alt='推荐模型1' width='1000px'></img> \n" +
// "#### 2. 深度学习的故障诊断 \n " +
// "![推荐模型2](../assets/recommend-model-2.png '深度学习的故障诊断')"


// 关于如何使用预定义的模型和加载已经保存的模型的介绍
const howToUseTemplateModel = "### 如何使用预定义的模型？ \n " +
    "#### 1. 点击左侧菜单栏中顶部的“系统模型库”，进入模型加载区。 \n" +
    "#### 2. 点击菜单栏中的“打开模型库”按钮，打开系统模型库界面。 \n" +
    "#### 3. 在系统模型库中，包含所有系统用户开发并保存的模型，可以直接使用，同时可以对本系统用户创建的模型进行管理。 \n"

const howToUseTemplateModel2 = "### 如何使用预定义的模型？ \n " +
    "#### 1. 点击菜单栏中的“打开模型库”按钮，打开系统模型库界面。 \n" +
    "#### 2. 在系统模型库中，包含所有系统用户开发并保存的模型，作为普通用户可以直接使用。 \n"


// 确认上传文件对话框
const uploadconfirmLoading = ref<boolean>(false);
const uploadConfirmDialog = ref<boolean>(false);
// 确保弹出的确认上传文件对话框位于最顶层
// const getContainer = () => document.body;

const dataFileFormState = ref({
  filename: "",
  description: "",
  multipleSensors: 'single',
  isPublic: 'private',
});
const fileUploadFormRef = ref();
const fileNameRules: Record<string, Rule[]> = {
  filename: [
    {required: true, message: "请输入文件名", trigger: "blur"},
    // { pattern: /[<>:"\/\\|?*]/, message: '文件名中包含非法字符', trigger: 'blur' }
    {pattern: /^[\u4e00-\u9fa5_a-zA-Z0-9]+$/, message: '请输入中英文/数字/下划线', trigger: 'blur'},
    // { validator: validateFilename, trigger: 'blur' }
  ],
  description: [
    {required: true, message: "请输入文件描述", trigger: "blur"},
  ],
  multipleSensors: [
    {required: true, message: "请选择是否为多传感器数据", trigger: "blur"},
  ],
}

// 文件名不能为'无'
// function validateFilename(rule, value, callback) {
//   if (value === '无') {
//     callback(new Error('文件名不能为“无”'));
//   } else {
//     callback();
//   }
// }


// 确认上传文件
const onFinish = () => {
  uploadconfirmLoading.value = true;
  const formData = new FormData();
  formData.append("file", fileList.value[0]);
  formData.append("filename", dataFileFormState.value.filename);
  formData.append("description", dataFileFormState.value.description);
  formData.append("multipleSensors", dataFileFormState.value.multipleSensors);
  formData.append("isPublic", dataFileFormState.value.isPublic);
  uploading.value = true;

  api.post("/user/upload_datafile/", formData)
      .then((response: any) => {
        if (response.data.message == 'save data success') {
          fileList.value = [];
          uploading.value = false;
          message.success("数据文件上传成功");

          uploadconfirmLoading.value = false;
          uploadConfirmDialog.value = false;
        } else {
          uploading.value = false;
          message.error("文件上传失败, " + response.data.message);
          uploadconfirmLoading.value = false;
        }
        if (response.data.code == 401) {
          ElMessageBox.alert('登录状态已失效，请重新登陆', '提示', {
            confirmButtonText: '确定',
            callback: (action: Action) => {
              router.push('/')
            },
          })
        }

      })
      .catch((error: any) => {
        uploading.value = false;
        uploadconfirmLoading.value = false;
        message.error("上传失败, " + error);
      });

};

const fileList = ref<UploadProps["fileList"]>([]);  // 文件列表
const uploading = ref<boolean>(false);
const loadingDataModel = ref<number>(1)

// 移除文件列表中的文件
const handleRemove: UploadProps["onRemove"] = (file) => {
  const index = fileList.value.indexOf(file);
  const newFileList = fileList.value.slice();
  newFileList.splice(index, 1);
  fileList.value = newFileList;
};

const beforeUpload: UploadProps["beforeUpload"] = (file) => {
  const allowedTypes = ['.npy', '.mat'];
  const fileType = file.name.split('.').pop().toLowerCase();
  if (!allowedTypes.includes('.' + fileType)) {
    ElMessage({
      message: '文件格式错误，请上传mat或npy文件',
      type: 'error',
    });
    return false;
  }

  fileList.value.length = 0;
  fileList.value = [...(fileList.value || []), file];
  return false;
};

// 文件类型检查，只允许mat或是npy格式的文件
// const handleUploadDataFile = () => {
//   let file = fileList.value[0]
//   let filename = file.name
//   const ext = filename.split('.').pop().toLowerCase();
//   if (ext != 'mat' && ext != 'npy') {
//     ElMessage({
//       message: '文件格式错误，请上传mat或npy文件',
//       type: 'error',
//     })
//     return
//   }
//   uploadConfirmDialog.value = true

// };

// 子组件向父组件发送数据
// const emit = defineEmits(["switchDrawer"]);

const switchDrawer = () => {
  let url = 'user/fetch_datafiles/'
  api.get(url)
      .then((response: any) => {
        let datasetInfo = response.data
        modelsDrawer.value = false;

        fetchedDataFiles.value = []

        for (let item of datasetInfo) {
          fetchedDataFiles.value.push(item)
        }

        dataDrawer.value = true
        // emit("switchDrawer", fetchedDatasetsInfo);
      })

  // fetchData.forEach(element => {
  //   fetchedDataFiles.value.push(element)
  // });

};

const operationHelpDialogVisible = ref(false)  // 用户操作指南对话框
const userHelpDialogVisible = ref(false)       // 用户使用教程对话框
const userHelpDialogScrollbar = ref(null)
// 用户权限
const modelSelection = ref("customModel");

// 私有算法列表
const privateAlgorithmList = ref([])

const extraAlgorithmStatement = ref({})


// 额外算法的描述
// const extraAlgorithmStatement = ref('')

const getExtraAlgorithm = (item: any) => {

  let algorithmTypeMapping = {
    '插值处理': "private_interpolation", '特征选择': 'extra_feature_selection',
    '特征提取': 'private_feature_extraction', '无量纲化': 'private_scale',
    '小波变换': 'extra_wavelet_transform', '故障诊断': 'private_fault_diagnosis',
    '故障预测': 'private_fault_prediction', '健康评估': 'extra_health_evaluation'
  }


  //获取私有算法列表
  // 如果是故障诊断的私有算法，则需要根据具体是机器学习的故障诊断还是深度学习的故障诊断进行分类
  var algorithmType  // 私有算法类型
  if (item.label != '故障诊断') {
    algorithmType = algorithmTypeMapping[item.label]
  } else {
    if (item.label_display.indexOf('机器学习') != -1) {
      algorithmType = 'private_fault_diagnosis_ml'  //机器学习算法的故障诊断
    } else {
      algorithmType = 'private_fault_diagnosis_dl'  //深度学习算法的故障诊断
    }
  }

  api.get('/user/user_fetch_private_algorithm?algorithm_type=' + algorithmType).then((response) => {
    if (response.data.code == 200) {
      // 将字符串数组转换为对象数组
      const algorithmList = response.data.algorithmList
      console.log("algorithmList: ", algorithmList)
      const algorithms = algorithmList.map(item => ({label: item.algorithmAlias}))
      // extraAlgorithmStatement.value = algorithmList.map(item => ( { 'item.algorithmAlias': item.algorithmStatement }))

      algorithmList.forEach(element => {
        extraAlgorithmStatement.value[element.algorithmAlias] = element.algorithmStatement
      });

      console.log(extraAlgorithmStatement.value)
      privateAlgorithmList.value.length = 0
      privateAlgorithmList.value = algorithms

    }
    if (response.data.code == 401) {
      ElMessageBox.alert('登录状态已失效，请重新登陆', '提示',
          {
            confirmButtonText: '确定',
            callback: (action: Action) => {
              router.push('/')
            }
          }
      )
    }

  })
      .catch(error => {
        ElMessage({
          message: '获取私有算法列表失败,' + error,
          type: 'error'
        })
      })
}


// 保存模型时提交的模型名的规则验证
const rules = {
  name: [
    {required: true, message: "请输入模型名", trigger: "blur"},
    // { pattern:/^[\u4e00-\u9fa5_a-zA-Z0-9]+$/, message: '请输入中英文/数字/下划线', trigger: 'blur' },
    {validator: validateModelname, trigger: 'blur'}
  ],
  description: [
    {required: true, message: "请输入模型描述", trigger: "blur"},
    {min: 1, max: 300, message: '长度应在1到300个字符之间', trigger: 'blur'}
  ],
  classify: [
    {required: true, message: "请选择分类", trigger: "blur"},
  ]
}

// 保存模型时模型名不能为'无'
function validateModelname(rule, value, callback) {
  if (value === '无') {
    callback(new Error('模型名不能为“无”'));
  } else {
    callback();
  }
}

// 在使用教程中滚动到指定部分的方法
const scrollTo = (sectionId: any) => {
  if (userHelpDialogScrollbar.value) {
    const element = userHelpDialogScrollbar.value.querySelector(`#${sectionId}`);
    if (element) {
      userHelpDialogScrollbar.value.scrollTop = element.offsetTop;
    }
  }
};

const router = useRouter()  // 页面路由

const dialogVisible = ref(false)

const activeName = ref('first')    // 控制标签页

const modelsDrawer = ref(false)   // 控制模型列表的抽屉
const dataDrawer = ref(false)     // 控制数据文件的抽屉

//控制按钮失效变量
const canStartProcess = ref(true)

const canCompleteModeling = computed(() => {
  if (nodeList.value.length > 0 && !modelHasBeenSaved) {
    return false
  } else {
    return true
  }
})
const canCheckModel = ref(true)
const canSaveModel = ref(true)
const canShutdown = ref(true)

// menuList2是为了显示算法列表，以及完成算法参数定义等操作，所定义的数据结构
// 其中节点的id为算法的id，label为算法的名称，parameters为算法的参数，use_algorithm为当前该模块所使用的算法名称，tip_show为是否显示提示信息的标志，tip为提示信息
const menuList2 = ref([
  {
    label: '数据预处理', id: '1', options: [
      {
        label: '插值处理', id: '1.1', use_algorithm: null, parameters: {
          'neighboring_values_interpolation': {},
          'bicubic_interpolation': {},
          'lagrange_interpolation': {},
          'newton_interpolation': {},
          'linear_interpolation': {},
          'deeplearning_interpolation': {},
        }, tip_show: false, tip: '对输入信号进行插值', optional: false
      },
      {
        label: '特征提取', id: '1.2', use_algorithm: null, parameters: {
          'time_domain_features': {
            均值: false,
            方差: false,
            标准差: false,
            偏度: false,
            峰度: false,
            四阶累积量: false,
            六阶累积量: false,
            最大值: false,
            最小值: false,
            中位数: false,
            峰峰值: false,
            整流平均值: false,
            均方根: false,
            方根幅值: false,
            波形因子: false,
            峰值因子: false,
            脉冲因子: false,
            裕度因子: false
          },
          'frequency_domain_features': {
            重心频率: false,
            均方频率: false,
            均方根频率: false,
            频率方差: false,
            频率标准差: false,
            谱峭度的均值: false,
            谱峭度的峰度: false,
          },
          'time_frequency_domain_features': {
            均值: false,
            方差: false,
            标准差: false,
            峰度: false,
            偏度: false,
            四阶累积量: false,
            六阶累积量: false,
            最大值: false,
            最小值: false,
            中位数: false,
            峰峰值: false,
            整流平均值: false,
            均方根: false,
            方根幅值: false,
            波形因子: false,
            峰值因子: false,
            脉冲因子: false,
            裕度因子: false,
            重心频率: false,
            均方频率: false,
            均方根频率: false,
            频率方差: false,
            频率标准差: false,
            谱峭度的均值: false,
            谱峭度的峰度: false,
          },
          'time_domain_features_multiple': {
            均值: false,
            方差: false,
            标准差: false,
            偏度: false,
            峰度: false,
            四阶累积量: false,
            六阶累积量: false,
            最大值: false,
            最小值: false,
            中位数: false,
            峰峰值: false,
            整流平均值: false,
            均方根: false,
            方根幅值: false,
            波形因子: false,
            峰值因子: false,
            脉冲因子: false,
            裕度因子: false
          },
          'frequency_domain_features_multiple': {
            重心频率: false,
            均方频率: false,
            均方根频率: false,
            频率方差: false,
            频率标准差: false,
            谱峭度的均值: false,
            谱峭度的峰度: false,
          },
          'time_frequency_domain_features_multiple': {
            均值: false,
            方差: false,
            标准差: false,
            峰度: false,
            偏度: false,
            四阶累积量: false,
            六阶累积量: false,
            最大值: false,
            最小值: false,
            中位数: false,
            峰峰值: false,
            整流平均值: false,
            均方根: false,
            方根幅值: false,
            波形因子: false,
            峰值因子: false,
            脉冲因子: false,
            裕度因子: false,
            重心频率: false,
            均方频率: false,
            均方根频率: false,
            频率方差: false,
            频率标准差: false,
            谱峭度的均值: false,
            谱峭度的峰度: false
          },
        }, tip_show: false, tip: '手工提取输入信号的特征', optional: true
      },
      {
        label: '无量纲化', id: '1.5', use_algorithm: null, parameters: {
          'max_min': {useLog: false},
          'z_score': {useLog: false},
          'robust_scaler': {useLog: false},
          'max_abs_scaler': {useLog: false},
        }, tip_show: false, tip: '对输入数据进行无量纲化处理', optional: true
      },
      {
        label: '特征选择', id: '1.3', use_algorithm: null, parameters: {
          'feature_imp': {rule: 1, threshold1: 0.1, threshold2: 0.1},
          'mutual_information_importance': {rule: 1, threshold1: 0.1, threshold2: 0.1},
          'correlation_coefficient_importance': {rule: 1, threshold1: 0.1, threshold2: 0.1},
          'feature_imp_multiple': {rule: 1, threshold1: 0.1, threshold2: 0.1},
          'mutual_information_importance_multiple': {rule: 1, threshold1: 0.1, threshold2: 0.1},
          'correlation_coefficient_importance_multiple': {rule: 1, threshold1: 0.1, threshold2: 0.1},
        }, tip_show: false, tip: '对提取到的特征进行特征选择', optional: true
      },
      {
        label: '小波变换', id: '1.4', use_algorithm: null, parameters: {
          'wavelet_trans_denoise': {'wavelet': 'db1', 'wavelet_level': '1'},
        }, tip_show: false, tip: '对输入信号进行小波变换', optional: true
      }
    ], tip_show: false, tip: '包含添加噪声、插值以及特征提取等'
  },
  {
    label: '故障检测', id: '2', options: [
      {
        label: '故障诊断', id: '2.1', use_algorithm: null, parameters: {
          'random_forest': {},
          'svc': {},
          'gru': {},
          'lstm': {},
          'random_forest_multiple': {},
          'svc_multiple': {},
          'gru_multiple': {},
          'lstm_multiple': {},
          'ulcnn': {},
          'ulcnn_multiple': {},
          'spectrumModel': {},
          'spectrumModel_multiple': {},
          'additional_model_one_multiple': {},
          'additional_model_two_multiple': {},
          'additional_model_three_multiple': {},
          'additional_model_four_multiple': {},
          'additional_model_five': {},
          'additional_model_six': {},
          'additional_model_seven': {},
          // 'private_fault_diagnosis_deeplearning': '',
        }, tip_show: false, tip: '根据提取特征对输入信号作故障诊断', optional: false
      },
      {
        label: '故障预测', id: '2.2', use_algorithm: null, parameters: {
          'linear_regression': {},
          'linear_regression_multiple': {},
        }, tip_show: false, tip: '根据提取的信号特征对输入信号进行故障预测', optional: false
      }]
  },
  {
    label: '健康评估', id: '3', options: [
      {
        label: '层次分析模糊综合评估', id: '3.1', use_algorithm: null, parameters: {
          'FAHP': {},
          'FAHP_multiple': {},
        }, tip_show: false, tip: '将模糊综合评价法和层次分析法相结合的评价方法', optional: false
      },
      {
        label: '层次朴素贝叶斯评估', id: '3.2', use_algorithm: null, parameters: {
          'BHM': {},
          'BHM_multiple': {},
        }, tip_show: false, tip: '使用朴素贝叶斯方法的评价方法', optional: false
      },
      {
        label: '层次逻辑回归评估', id: '3.3', use_algorithm: null, parameters: {
          'AHP': {},
          'AHP_multiple': {},
        }, tip_show: false, tip: '使用层次逻辑回归方法的评价方法', optional: false
      },
    ]
  },
]);


// 算法参数的推荐值，目前包括小波变换的变换类型和变换层数、特征选择的依据规则及相应阈值
const recommendParams = {
  'wavelet': [{value: 'db1', label: 'db1'}, {value: 'db2', label: 'db2'}, {value: 'sym2', label: 'sym2'}, {value: 'coif1', label: 'coif1'}],
  'wavelet_level': [{value: 1, label: '1'}, {value: 2, label: '2'}, {value: 3, label: '3'}],
  // 规则一的各算法的阈值推荐值
  'threshold1': {
    'feature_imp': [{value: 0.005, label: '0.005'}, {value: 0.01, label: '0.01'}, {
      value: 0.02,
      label: '0.02'
    }, {value: 0.03, label: '0.03'}, {value: 0.04, label: '0.04'}, {value: 0.05, label: 0.05}, {
      value: 0.1,
      label: 0.1
    }],
    'mutual_information_importance': [{value: 0.1, label: '0.1'}, {value: 0.2, label: '0.2'}, {
      value: 0.3,
      label: '0.3'
    }, {value: 0.4, label: '0.4'}, {value: 0.5, label: '0.5'}, {value: 0.6, label: '0.6'},],
    'mutual_information_importance_multiple': [{value: 0.3, label: '0.3'}, {value: 0.35, label: '0.35'}, {
      value: 0.4,
      label: '0.4'
    }, {value: 0.45, label: '0.45'}, {value: 0.5, label: '0.5'}],
    'feature_imp_multiple': [{value: 0.01, label: '0.01'}, {value: 0.03, label: '0.03'}, {
      value: 0.05,
      label: '0.05'
    }, {value: 0.06, label: '0.06'}],
    'correlation_coefficient_importance_multiple': [{value: 0.58, label: '0.58'}, {
      value: 0.6,
      label: '0.6'
    }, {value: 0.62, label: '0.62'}, {value: 0.64, label: '0.64'}],
    'correlation_coefficient_importance': [{value: 0.1, label: '0.1'}, {value: 0.2, label: '0.2'}, {
      value: 0.3,
      label: '0.3'
    }, {value: 0.4, label: '0.4'}, {value: 0.5, label: '0.5'}, {value: 0.6, label: '0.6'},]
  },

  // 规则二的各算法的阈值推荐值
  'threshold2': {
    'feature_imp': [{value: 0.3, label: '0.3'}, {value: 0.4, label: '0.4'}, {value: 0.5, label: '0.5'}, {
      value: 0.6,
      label: '0.6'
    }, {value: 0.7, label: '0.7'}, {value: 0.8, label: '0.8'}, {value: 1, label: 1}],
    'mutual_information_importance': [{value: 0.3, label: '0.3'}, {value: 0.4, label: '0.4'}, {
      value: 0.5,
      label: '0.5'
    }, {value: 0.6, label: '0.6'}, {value: 0.7, label: '0.7'}, {value: 0.8, label: '0.8'}, {value: 1, label: 1}],
    'feature_imp_multiple': [{value: 0.3, label: '0.3'}, {value: 0.4, label: '0.4'}, {
      value: 0.5,
      label: '0.5'
    }, {value: 0.6, label: '0.6'}, {value: 0.7, label: '0.7'}, {value: 0.8, label: '0.8'}, {value: 1, label: 1}],
    'mutual_information_importance_multiple': [{value: 0.3, label: '0.3'}, {value: 0.4, label: '0.4'}, {
      value: 0.5,
      label: '0.5'
    }, {value: 0.6, label: '0.6'}, {value: 0.7, label: '0.7'}, {value: 0.8, label: '0.8'}, {value: 1, label: 1}],
    'correlation_coefficient_importance_multiple': [{value: 0.2, label: '0.2'}, {value: 0.3, label: '0.3'}, {
      value: 0.4,
      label: '0.4'
    }, {value: 0.5, label: '0.5'}, {value: 0.6, label: '0.6'}, {value: 0.7, label: '0.7'}, {
      value: 0.8,
      label: '0.8'
    }, {value: 1, label: 1}],
    'correlation_coefficient_importance': [{value: 0.3, label: '0.3'}, {value: 0.4, label: '0.4'}, {
      value: 0.5,
      label: '0.5'
    }, {value: 0.6, label: '0.6'}, {value: 0.7, label: '0.7'}, {value: 0.8, label: '0.8'}, {value: 1, label: 1}]
  },
  // 'thresholdImpSingle1': [{value: 0.005, label: '0.005'}, {value: 0.01, label: '0.01'}, {value: 0.02, label: '0.02'}, {value: 0.03, label: '0.03'}, {value: 0.04, label: '0.04'}, {value: 0.05, label: 0.05}, {value: 0.1, label: 0.1}],
  // 'thresholdImgSingle2': [{value: 0.3, label: '0.3'}, {value: 0.4, label: '0.4'}, {value: 0.5, label: '0.5'}, {value: 0.6, label: '0.6'}, {value: 0.7, label: '0.7'}, {value: 0.8, label: '0.8'}, {value: 1, label: 1}]
  'scaleUseLogs': [{value: true, label: '使用训练模型时对数据的标准化方法'}, {
    value: false,
    label: '不使用训练模型时对数据的标准化方法'
  }]
}


// 监听特征选择的规则对应的阈值的初始值，以适应性的调整阈值的初始值

// 用于显示算法介绍
const introductionToShow = ref('# 你好世界')  // 需要展示在可视化建模区的算法介绍
const showPlainIntroduction = ref(false)


// 算法介绍，点击算法选择区内的具体算法，将其算法介绍展示在可视化建模区
const showIntroduction = (algorithm: string) => {
  resultsViewClear()
  showStatusMessage.value = false
  showPlainIntroduction.value = true
  introductionToShow.value = plainIntroduction[algorithm]

  showResultOfElMain(); //这里加了一句显示结果展示区域(若被隐藏)
}

// 算法选择菜单下拉展示
const menuDetailsSecond = ref<{ [key: string]: boolean }>({});

const menuDetailsThird = ref({})


// 点击二级目录进行展开时，在结果可视化区域显示对应二级目录功能下所有算法的优劣比较
const contrastVisible = ref(false);

// 当点击二级目录时，展示对应三级目录下所有算法的优劣，此处为不同模块下各个算法优劣比较的表格的markdown代码

const contrastToShow = ref('')

const clickAtSecondMenu = (option: any) => {
  // 当点击二级目录时，展开对应二级目录下的三级目录
  menuDetailsThird.value[option.label] = !menuDetailsThird.value[option.label]

  // 在结果可视化区域显示对应二级目录功能下所有算法的优劣比较
  let secondAlgorithm = option.label
  if (secondAlgorithm === '层次分析模糊综合评估' || secondAlgorithm === '层次朴素贝叶斯评估' || secondAlgorithm === '层次逻辑回归评估' || secondAlgorithm === '健康评估') {
    secondAlgorithm = '层次分析健康评估'
  }
  contrastToShow.value = contrastOfAlgorithm[secondAlgorithm]

  resultsViewClear()
  contrastVisible.value = true
}

// 特征提取所选择的特征
// const features = ref(['均值', '方差', '标准差', '峰度', '偏度', '四阶累积量', '六阶累积量', '最大值', '最小值', '中位数', '峰峰值', '整流平均值', '均方根', '方根幅值',
//   '波形因子', '峰值因子', '脉冲因子', '裕度因子', '重心频率', '均方频率', '均方根频率', '频率方差', '频率标准差', '谱峭度的均值', '谱峭度的峰度'])
const features = ref([])

//双向链表用于存储调用的模块顺序
class ListNode {
  constructor(value) {
    this.value = value;
    this.next = null;
  }
}

class LinkedList {
  constructor() {
    this.head = null;
    this.tail = null;
  }

  // 添加新元素到链表尾部
  append(value) {
    const newNode = new ListNode(value);

    if (!this.head) {
      this.head = newNode;
      this.tail = newNode;
    } else {
      this.tail.next = newNode;
      this.tail = newNode;
    }
  }

  // 在链表的头部添加新节点
  insertAtHead(value) {
    const newNode = new ListNode(value);

    if (!this.head) {
      this.head = newNode;
      this.tail = newNode;
    } else {
      newNode.next = this.head;
      this.head = newNode;
    }
  }

  // 打印链表所有元素
  print() {
    let current = this.head;
    while (current) {
      console.log(current.value);
      current = current.next;
    }
  }

  get_all_nodes() {
    let current = this.head;
    let nodeList = []
    while (current) {
      nodeList.push(current.value)
      current = current.next;
    }
    return nodeList
  }

  length() {
    if (this.head) {
      let len = 1
      let p = this.head.next
      while (p) {
        p = p.next
        len += 1
      }
      return len
    }
    return 0
  }

  search(target_value) {
    if (this.head == null) {
      return false
    } else {
      let current = this.head
      while (current) {
        if (current.value == target_value) {
          return current
        }
        current = current.next
      }
      return false
    }
  }

  searchPre(targetValue) {
    if (this.head == null) {
      return false
    } else {
      let current = this.head
      while (current && current.next) {
        if (current.next.value == targetValue) {
          return current
        }
        current = current.next
      }
      return false
    }
  }
}

const logout = () => {
  router.push('/')
}

// 标签与节点id的转换
const displayLabelToId = (displayLabel) => {
  nodeList.value.forEach(node => {
    if (node.display_label == displayLabel) {
      return node.id
    }
  })
}

// 节点标签到节点标识id的转换
function labelToId(label) {
  let nodeList1 = nodeList.value.slice()
  let nodeIdToFind = 0
  nodeList1.forEach(node => {
    if (node.label == label) {
      nodeIdToFind = node.id
    }
  })
  return nodeIdToFind
}

const userRole = ref('');  // 用户登录时所选择的角色，用于区分超级用户和普通用户的不同界面

// 将建立模型的连线操作、用户名设置、区分普通用户和系统用户的功能, 挂在到onMounted中
const linkedList = new LinkedList()
onMounted(() => {
  // fetchComponentTrees();
  //新增的elmain start
  // loadStateOfElMain()
  // 添加resize事件监听器，使用节流后的函数
  // window.addEventListener('resize', updateMaxHeightOfElMain)
  window.addEventListener('resize', throttledHandleResize);
  // window.addEventListener('beforeunload', saveStateOfElMain)
  //新增的elmain start

  username.value = window.sessionStorage.getItem('username') || '用户名未设置'
  userRole.value = window.sessionStorage.getItem('role') || '无效的用户'
  // console.log('username: ', username.value)
  console.log('userRole: ', userRole.value)
  //获取用户上传的增值组件并构造对应的目录结构体
  getExtraAlgorithmMao()
  // 当进行建模的时候隐藏可视化建模区的背景文字
  document.querySelector('.el-main').classList.add('has-background');
  plumbIns = jsPlumb.getInstance()
  jsPlumbInit()

  

  plumbIns.bind("connection", function (info) {
    let sourceId = info.connection.sourceId
    let targetId = info.connection.targetId

    let id_to_label = {}

    nodeList.value.forEach(node => {
      let id = node.id
      let label = node.label
      id_to_label[id] = label
    })
    if (linkedList.head == null) {
      linkedList.append(id_to_label[sourceId])
      linkedList.append(id_to_label[targetId])
    } else {
      if (linkedList.head.value == id_to_label[targetId]) {
        linkedList.insertAtHead(id_to_label[sourceId])
      } else {
        linkedList.append(id_to_label[targetId])
      }
    }
    // 除去在linkedList中的节点，其他节点不能作为连线操作的出发点
    let linked = linkedList.get_all_nodes()
    // for(let [value, key] of id_to_label){
    //   if (linked.indexOf(key) == -1){
    //     plumbIns
    //   }
    // }
    // console.log('linked: ' + linked)
  })
})

const deff = {
  jsplumbSetting: {
    // 动态锚点、位置自适应
    Anchors: ['Right', 'Left'],
    anchor: ['Right', 'Left'],
    // 容器ID
    Container: 'efContainer',
    // 连线的样式，直线或者曲线等，可选值:  StateMachine、Flowchart，Bezier、Straight
    // Connector: ['Bezier', {curviness: 100}],
    // Connector: ['Straight', { stub: 20, gap: 1 }],
    Connector: ['Flowchart', {stub: 30, gap: 1, alwaysRespectStubs: false, midpoint: 0.5, cornerRadius: 10}],
    // Connector: ['StateMachine', {margin: 5, curviness: 10, proximityLimit: 80}],
    // 鼠标不能拖动删除线
    ConnectionsDetachable: false,
    // 删除线的时候节点不删除
    DeleteEndpointsOnDetach: false,
    /**
     * 连线的两端端点类型：圆形
     * radius: 圆的半径，越大圆越大
     */
    Endpoint: ['Dot', {radius: 8, cssClass: 'ef-dot', hoverClass: 'ef-dot-hover'}],

    EndpointStyle: {fill: '#808080', outlineWidth: 3,},
    // 是否打开jsPlumb的内部日志记录
    LogEnabled: true,
    /**
     * 连线的样式
     */
    PaintStyle: {
      // 线的颜色
      stroke: '#808080',
      // 线的粗细，值越大线越粗
      strokeWidth: 7,
      // 设置外边线的颜色，默认设置透明
      outlineStroke: 'transparent',
      // 线外边的宽，值越大，线的点击范围越大
      outlineWidth: 5,
    },
    DragOptions: {cursor: 'pointer', zIndex: 2000},
    ConnectionOverlays: [
      ['Custom', {
        create() {
          const el = document.createElement('div')
          // el.innerHTML = '<select id=\'myDropDown\'><option value=\'foo\'>foo</option><option value=\'bar\'>bar</option></select>'
          return el
        },
        location: 0.7,
        id: 'customOverlay',
      }],
    ],

    Overlays: [
      // 箭头叠加
      ['Arrow', {
        width: 25, // 箭头尾部的宽度
        length: 8, // 从箭头的尾部到头部的距离
        location: 1, // 位置，建议使用0～1之间
        direction: 1, // 方向，默认值为1（表示向前），可选-1（表示向后）
        foldback: 0.623, // 折回，也就是尾翼的角度，默认0.623，当为1时，为正三角
      }],

      ['Label', {label: '', location: 0.1, cssClass: 'aLabel',}],

    ],
    // 绘制图的模式 svg、canvas
    RenderMode: 'canvas',
    // 鼠标滑过线的样式
    HoverPaintStyle: {stroke: '#808080', strokeWidth: 10},
    // 滑过锚点效果
    EndpointHoverStyle: {fill: '#808080'},
    Scope: 'jsPlumb_DefaultScope', // 范围，具有相同scope的点才可连接
  },
  /**
   * 连线参数
   */
  jsplumbConnectOptions: {
    isSource: true,
    isTarget: true,
    // 动态锚点、提供了4个方向 Continuous、AutoDefault
    // anchor: 'Continuous',
    // anchor: ['Continuous', { faces: ['left', 'right'] }],
    // 设置连线上面的label样式
    labelStyle: {
      cssClass: 'flowLabel',
    },
  },
  /**
   * 源点配置参数
   */
  jsplumbSourceOptions: {
    // 设置可以拖拽的类名，只要鼠标移动到该类名上的DOM，就可以拖拽连线
    filter: '.node-drag',
    filterExclude: false,
    anchor: ['Continuous', {faces: ['right']}],
    // 是否允许自己连接自己
    allowLoopback: false,
    maxConnections: -1,
  },

  jsplumbSourceOptions2: {
    // 设置可以拖拽的类名，只要鼠标移动到该类名上的DOM，就可以拖拽连线
    filter: '.node-drag',
    filterExclude: false,
    // anchor: 'Continuous',
    // 是否允许自己连接自己
    allowLoopback: true,
    connector: ['Flowchart', {curviness: 50}],
    connectorStyle: {
      // 线的颜色
      stroke: 'red',
      // 线的粗细，值越大线越粗
      strokeWidth: 1,
      // 设置外边线的颜色，默认设置透明
      outlineStroke: 'transparent',
      // 线外边的宽，值越大，线的点击范围越大
      outlineWidth: 10,
    },
    connectorHoverStyle: {stroke: 'red', strokeWidth: 2},
  },
  jsplumbTargetOptions: {
    // 设置可以拖拽的类名，只要鼠标移动到该类名上的DOM，就可以拖拽连线
    filter: '.node-drag',
    filterExclude: false,
    // 是否允许自己连接自己
    anchor: ['Continuous', {faces: ['left']}],
    allowLoopback: false,
    dropOptions: {hoverClass: 'ef-drop-hover'},
  },
}


const done = ref(false)      // 控制模型是否可以拖拽，当其值为true时不可拖拽模型
const dialogModle = ref(false)  // 保存模型对话框框

let modelCheckRight = false  // 为真时表明通过模型检查

// 检查模型
const checkModel = () => {
  console.log("进入检查模型", linkedList.get_all_nodes())
  let idToModule = {}
  let algorithms = []
  let algorithmSchedule = []
  let moduleSchedule = []
  // 如果只有一个模块则不需要建立流程
  if (nodeList.value.length == 1) {
    moduleSchedule.push(nodeList.value[0].label)  // 模块名称拼接的字符串
    algorithmSchedule.push(nodeList.value[0].label_display)  // 算法名称拼接的字符串
    // 根据是否包含多传感器的算法，判断是否是针对多传感器的模型
    if (algorithmSchedule.indexOf("多传感器") != -1) {
      contentJson.multipleSensor = true  // 默认为false，即对单传感器数据的模型
    }
  } else {

    // 如果有多个模块则需要根据用户的连接动作去形成正确的模型流程
    let allConnections = plumbIns.getConnections();
    console.log('all_connections: ', allConnections)
    // 获取连线元素的单向映射
    let connectionsMap: any = {};
    allConnections.forEach(connection => {
      const sourceId = connection.sourceId;
      const targetId = connection.targetId;

      // 如果源元素ID不在connectionsMap中，则初始化为空数组
      if (!connectionsMap[sourceId]) {
        connectionsMap[sourceId] = [];
      }
      connectionsMap[sourceId].push(targetId);
    })

    // 寻找用户建立的模型流程逻辑上的第一个元素
    function findStartElement(connectionsMap: any) {
      // 创建一个集合来存储所有元素的ID
      const allElements = new Set(Object.keys(connectionsMap).concat(...Object.values(connectionsMap).map(list => list)));

      // 遍历所有元素，查找没有入度的元素
      for (const elementId of allElements) {
        let hasIncomingConnection = false;
        for (const connections of Object.values(connectionsMap)) {
          if (connections.includes(elementId)) {
            hasIncomingConnection = true;
            break;
          }
        }
        if (!hasIncomingConnection) {
          return elementId;     // 找到没有入度的元素，即起点
        }
      }

      // 如果没有找到没有入度的元素，则可能图不是线性的，或者connectionsMap构建有误
      throw new Error("未找到起点元素.");
    }

    let startElementId = findStartElement(connectionsMap);

    // 寻找逻辑上的下一个元素
    function findNextElementIdInSequence(currentElementId, connectionsMap) {

      const connections = connectionsMap[currentElementId];

      // 建立模型时，模型序列是线性的
      if (connections && connections.length > 0) {
        return connections[0]; // 返回序列中的下一个元素ID
      }
      return null;
    }

    // 生成所建立模型的运行流程
    function traverseLinearSequence(startElementId, connectionsMap, visited = new Set(), order = []) {
      // 检查是否已访问过当前元素
      if (visited.has(startElementId)) {
        return;
      }

      visited.add(startElementId); // 标记为已访问
      order.push(startElementId); // 将元素添加到顺序数组中

      let nextElementId = findNextElementIdInSequence(startElementId, connectionsMap);

      if (nextElementId !== null) {
        // 递归遍历下一个元素
        traverseLinearSequence(nextElementId, connectionsMap, visited, order);
      }
      // 最终返回模型的运行流程
      return order;
    }

    let sequenceOrder = traverseLinearSequence(startElementId, connectionsMap);
    console.log('sequenceOrder: ', sequenceOrder);
    nodeList.value.forEach(node => {
      let id = node.id
      let label = node.label
      let algorithm = node.label_display
      idToModule[id] = label
      algorithms.push(algorithm)
    })

    sequenceOrder.forEach(id => {
      moduleSchedule.push(idToModule[id])
    });

    // 形成表示具体算法模块连接顺序的字符串
    for (let i = 0; i < moduleSchedule.length; i++) {
      let module = moduleSchedule[i]
      nodeList.value.forEach(node => {
        if (node.label == module) {
          algorithmSchedule.push(node.label_display)
        }
      });
    }
  }


  let moduleStr = Object.values(moduleSchedule).join('')   // 所有模块的名称按顺序拼接起来的字符串
  let algorithmStr = Object.values(algorithmSchedule).join('')  // 所有模块中的算法名称按顺序拼接起来的字符串

  // 判断子串后是否有更多的文本
  const moreText = (text, substring) => {
    const position = text.indexOf(substring);
    if (position === -1) {
      return false;
    }
    const endPosition = position + substring.length;
    return endPosition < text.length;
  }

  const includeHealthEvaluation = (moduleStr: string) => {
    if (moduleStr.match('层次分析模糊综合评估')) {
      return '层次分析模糊综合评估';
    } else if (moduleStr.match('层次朴素贝叶斯评估')) {
      return '层次朴素贝叶斯评估';
    } else if (moduleStr.match('层次逻辑回归评估')) {
      return '层次逻辑回归评估';
    } else if (moduleStr.match('健康评估')) {
      return '健康评估';
    } else {
      return '';
    }
  }

  // 判断一个子串后是否有另一个子串，其中subStrs2为包含需要寻找的子串的数组
  const checkSubstrings = (str, subStr1, subStrs2) => {
    const index1 = str.indexOf(subStr1);
    if (index1 !== -1) {
      // 如果 subStr1 存在
      for (const subStr2 of subStrs2) {
        const index2 = str.indexOf(subStr2, index1 + subStr1.length);
        if (index2 !== -1) {
          // 如果在 subStr1 之后找到了 subStr2 中的任何一个则返回true
          return true;
        }
      }
    }
    return false;
  }
  if (nodeList.value.length) {
    // 首先判断模型中是否有数据源
    if (!moduleStr.match('数据源')) {
      ElMessage.error('模型中未包含数据源，请添加数据源模块')
      return
    } else {
      if (nodeList.value.length == 1) {
        ElMessage.error('模型中仅包含数据源，无法运行，请添加其他模块')
        return
      }
      if (moduleStr.indexOf('数据源') > 0) {
        ElMessage.error('数据源模块必须位于模型中第一个位置')
        return
      }
    }
    moduleStr = moduleStr.replace('数据源', '')
    algorithmStr = algorithmStr.replace('数据源', '')
    console.log('moduleStr: ', moduleStr)
    console.log('algorithmStr: ', algorithmStr)
    // 首先判断模型中是否存在除了数据源之外的1个以上的模块，如果模型中只有一个模块，判断其是否可以独立地运行而不需要其他模块的支持
    if (nodeList.value.length == 2) {
      if (!moduleStr.match('插值处理') && !moduleStr.match('特征提取') && !algorithmStr.match('GRU的故障诊断') && !algorithmStr.match('LSTM的故障诊断') && !algorithmStr.match('小波变换')
          && !algorithmStr.match('一维卷积深度学习模型的故障诊断') && !algorithmStr.match('基于时频图的深度学习模型的故障诊断') && !moduleStr.match('无量纲化') && !algorithmStr.match('深度学习故障诊断')) {
        let tip
        if (moduleStr.match('故障诊断')) {
          tip = '模型中包含故障诊断，建议在此之前进行特征提取和特征选择等操作'
        } else if (moduleStr.match('层次分析模糊综合评估')) {
          tip = '模型中包含层次分析模糊综合评估，建议在此之前进行特征提取和特征选择等操作'
        } else if (moduleStr.match('特征选择')) {
          tip = '模型中包含特征选择，建议在此之前进行特征提取等操作'
        } else if (moduleStr.match('故障预测')) {
          tip = '模型中包含故障预测，建议在此之前进行故障诊断'
        }

        ElMessage({
          message: '该算法无法单独使用，请结合相应的算法,' + tip,
          type: 'warning',
          showClose: true
        })

        return
      } else {
        // 无量纲化要检查是否使用模型训练师使用的标准化方法，对输入的原始信号无法使用模型训练时使用的标准化方法进行无量纲化
        if (moduleStr.match('无量纲化')) {
          let node
          for (let item of modeling_nodeList.value) {
            if (item.nodeInfo.label == '无量纲化') {
              node = item.nodeInfo
              break
            }
          }
          if (node?.parameters[node.use_algorithm]['useLog'] == true) {

            ElMessageBox.alert('如果要使用模型训练时使用的标准化方法进行无量纲化，请确保无量纲化模块之前对数据进行了特征提取，或者在参数设置中选择不使用模型训练时使用的标准化方法', '提示', {
              confirmButtonText: '确定',
              draggable: true,
              buttonSize: 'medium',
            })

            return
          }
        }
        // 如果模块可以单独运行，再进行模型中各个模块的参数设置的检查
        let checkParamsRight = checkModelParam()
        let isLofical_completenessed = toObject().nodes.length-toObject().edges.length
        console.log('isLofical_completenessed: ', isLofical_completenessed)
        if (checkParamsRight && isLofical_completenessed!=1) {
          ElMessage({
            showClose: true,
            message: '模型正常，可以保存并运行',
            type: 'success'
          })
          modelCheckRight = true
          updateStatus('模型建立并已通过模型检查')
        } else {
          ElMessage({
            showClose: true,
            message: '请确保所有具有参数的模块的参数设置正确',
            type: 'warning'
          })
          return
        }
      }
    } else {
      // 检查模型中是否存在未被连接的模块
      if (linkedList.length() != nodeList.value.length) {
        ElMessage({
          message: '请确保图中所有模块均已建立连接，且没有多余的模块',
          type: 'warning'
        })
        return
      } else {
        // 模型正常连接的情况下进行模型逻辑以及模型参数的检查
        if (algorithmStr.match('多传感器') && algorithmStr.match('单传感器')) {
          ElMessage({
            showClose: true,
            message: '多传感器和单传感器的算法不能混合使用！',
            type: 'warning'
          })
          return
        }
        if (moduleStr.match('故障诊断')) {
          // 如果是深度学习模型的故障诊断
          if (algorithmStr.match('深度学习模型的故障诊断') || algorithmStr.match('GRU的故障诊断') || algorithmStr.match('LSTM的故障诊断')) {
            if (moduleStr.indexOf('故障诊断') > 0) {
              // 检查深度学习模型的故障诊断之前是否包含不必要的模块
              let preModuleText = moduleStr.substring(0, moduleStr.indexOf('故障诊断'))
              if (preModuleText.match('特征提取') || preModuleText.match('特征选择') || preModuleText.match('无量纲化') || preModuleText.match('故障预测')) {
                ElMessage({
                  message: '深度学习模型的故障诊断不需要人工提取特征，因此其之前不需要包含如特征提取、特征选择等不必要的模块！',
                  type: 'warning',
                  showClose: true
                })
                return
              }
            }
            // 如果使用深度学习模型的故障诊断之后有其他的模块
            if (moreText(moduleStr, '故障诊断')) {
              let nextModuleText = moduleStr.substring(moduleStr.indexOf('故障诊断'), moduleStr.length)  //故障诊断模块之后的其他模块名拼接的字符串
              if (nextModuleText.match('故障预测') || nextModuleText.match('层次分析模糊综合评估') || nextModuleText.match('层次朴素贝叶斯评估') || nextModuleText.match('层次逻辑回归评估')) {
                // 如果同时包含故障预测以及层次分析模糊综合评估
                let current: string
                if (nextModuleText.match('故障预测') && (nextModuleText.match('层次分析模糊综合评估') || nextModuleText.match('层次朴素贝叶斯评估') || nextModuleText.match('层次逻辑回归评估'))) {
                  // 获取健康评估模块所在的位置
                  let healthEvaluationIndex
                  if (nextModuleText.match('层次分析模糊综合评估')) {
                    healthEvaluationIndex = nextModuleText.indexOf('层次分析模糊综合评估')
                  } else if (nextModuleText.match('层次朴素贝叶斯评估')) {
                    healthEvaluationIndex = nextModuleText.indexOf('层次朴素贝叶斯评估')
                  } else {
                    healthEvaluationIndex = nextModuleText.indexOf('层次逻辑回归评估')
                  }
                  // 如果健康评估模块位置在深度学习的故障预测组件之后，需要进一步进行手工特征的提取
                  if (nextModuleText.indexOf('故障预测') > healthEvaluationIndex) {
                    ElMessage({
                      message: '注意故障预测应该在层次分析模糊综合评估之前运行',
                      type: 'warning',
                      showClose: true
                    })
                    return
                  } else {
                    current = '故障预测'
                  }
                }

                // 因为之前的深度学习模型的故障诊断无法为故障预测或是健康评估提供样本特征，因此需要进行特征提取和特征选择
                if (nextModuleText.indexOf('故障预测') == -1) {
                  current = includeHealthEvaluation(moduleStr)
                  if (!current) {
                    message.error('模型检查出错，请重新链接模型')
                    return
                  }
                } else {
                  current = '故障预测'
                }
                let preModuleText = nextModuleText.substring(0, nextModuleText.indexOf(current))
                if (!preModuleText.match('特征提取特征选择') && !preModuleText.match('特征提取无量纲化特征选择') && !preModuleText.match('特征提取特征选择无量纲化')) {
                  ElMessage({
                    message: '建议在深度学习模型的故障诊断之后包含特征提取和特征选择模块',
                    type: 'warning',
                    showClose: true
                  })
                  return
                }

              }
            }
          } else {
            // 如果是传统机器学习的故障诊断
            let preModuleText = moduleStr.substring(0, moduleStr.indexOf('故障诊断'))

            // 如果机器学习的故障诊断之前既不包含特征提取，也不包含特征选择
            if (!preModuleText.match('特征提取') && !preModuleText.match('特征选择')) {
              ElMessage({
                message: '建议在故障诊断之前进行特征提取和特征选择',
                type: 'warning',
                showClose: true
              })
              let preModule = linkedList.searchPre('故障诊断') // 寻找故障诊断之前的节点，即不符合规则的节点

              // 红色标明报错连线
              let sourceId = labelToId(preModule.value)
              let targetId = labelToId('故障诊断')

              plumbIns.select({source: sourceId, target: targetId}).setPaintStyle({
                stroke: '#E53935',
                strokeWidth: 7,
                outlineStroke: 'transparent',
                outlineWidth: 5,

              });
              return
            } else {
              // 如果特征提取和特征选择同时存在
              if (preModuleText.match('特征提取') && preModuleText.match('特征选择')) {
                // 如果特征提取在特征选择之后，此时逻辑错误
                if (preModuleText.indexOf('特征提取') > preModuleText.indexOf('特征选择')) {
                  ElMessage({
                    message: '建议在特征提取之后进行特征选择',
                    type: 'warning',
                    showClose: true
                  })
                  return
                }
              } else {
                // 如果只包含特征选择
                if (preModuleText.match('特征选择')) {
                  ElMessage({
                    message: '建议在特征提取之后再进行特征选择',
                    type: 'warning',
                    showClose: true
                  })
                  let preModule = linkedList.searchPre('特征选择') // 寻找特征选择之前的节点，即不符合规则的节点

                  // 红色标明报错连线
                  let sourceId = labelToId(preModule.value)
                  let targetId = labelToId('特征选择')

                  plumbIns.select({source: sourceId, target: targetId}).setPaintStyle({
                    stroke: '#E53935',
                    strokeWidth: 7,
                    outlineStroke: 'transparent',
                    outlineWidth: 5,

                  });
                  return
                }
                // 如果只包含特征提取
                else if (preModuleText.match('特征提取')) {
                  ElMessage({
                    message: '因模型中包含机器学习的故障诊断，建议在特征提取之后进行特征选择',
                    type: 'warning',
                    showClose: true
                  })
                  let current = linkedList.search('特征提取') // 寻找特征选择之前的节点，即不符合规则的节点
                  let next = current.next
                  // 红色标明报错连线
                  let sourceId = labelToId(current.value)
                  let targetId = labelToId(next.value)

                  plumbIns.select({source: sourceId, target: targetId}).setPaintStyle({
                    stroke: '#E53935',
                    strokeWidth: 7,
                    outlineStroke: 'transparent',
                    outlineWidth: 5,

                  });
                  return
                }

              }
            }
          }
        }

        if (moduleStr.match('特征提取故障诊断')) {
          let sourceId = labelToId('特征提取')
          let current = linkedList.search('特征提取')
          let next = current.next.value
          let targetId = labelToId(next)

          let connection = plumbIns.getConnections({source: sourceId, traget: targetId})
          console.log('connection: ', connection)

          plumbIns.select({source: sourceId, target: targetId}).setPaintStyle({
            stroke: '#E53935',
            strokeWidth: 7,
            outlineStroke: 'transparent',
            outlineWidth: 5,

          });
          ElMessage({
            showClose: true,
            message: '因模型中包含故障诊断，建议在特征提取之后包含特征选择',
            type: 'warning'
          })
          return
        }
        if (moduleStr.indexOf('小波变换') > 0) {
          // 小波变换只能针对信号序列，之前不能已经进行了特征提取
          let preModuleText = moduleStr.substring(0, moduleStr.indexOf('小波变换'))
          if (preModuleText.match('特征提取')) {
            ElMessage({
              showClose: true,
              message: '模型中对原始信号进行了特征提取，而小波变换只能针对信号序列',
              type: 'warning'
            })
            let preModule = linkedList.searchPre('小波变换') // 寻找健康评估之前的节点，即不符合规则的节点

            // 红色标明报错连线
            let sourceId = labelToId(preModule.value)
            let targetId = labelToId('小波变换')

            let connection = plumbIns.getConnections({source: sourceId, traget: targetId})
            console.log('connection: ', connection)

            plumbIns.select({source: sourceId, target: targetId}).setPaintStyle({
              stroke: '#E53935',
              strokeWidth: 7,
              outlineStroke: 'transparent',
              outlineWidth: 5,

            });
            return
          }
        }
        if (includeHealthEvaluation(moduleStr)) {

          let healthEvaluation = includeHealthEvaluation(moduleStr)  //所包含的健康评估的组件名
          if (!moduleStr.match('特征提取')) {
            ElMessage({
              showClose: true,
              message: '因模型中包含层次分析模糊综合评估，建议在此之前包含特征提取',
              type: 'warning'
            })
            let current = linkedList.searchPre(healthEvaluation) // 寻找健康评估之前的节点，即不符合规则的节点

            // 红色标明报错连线
            let sourceId = labelToId(current.value)
            let targetId = labelToId(healthEvaluation)

            let connection = plumbIns.getConnections({source: sourceId, traget: targetId})
            console.log('connection: ', connection)

            plumbIns.select({source: sourceId, target: targetId}).setPaintStyle({
              stroke: '#E53935',
              strokeWidth: 7,
              outlineStroke: 'transparent',
              outlineWidth: 5,
            });
            return
          }
          if (moreText(moduleStr, healthEvaluation)) {
            let sourceId = labelToId(healthEvaluation)
            let current = linkedList.search(healthEvaluation)
            let next = current.next.value
            let targetId = labelToId(next)

            plumbIns.select({source: sourceId, target: targetId}).setPaintStyle({
              stroke: '#E53935',
              strokeWidth: 7,
              outlineStroke: 'transparent',
              outlineWidth: 5,

            });
            ElMessage({
              showClose: true,
              message: '注意健康评估之后无法连接更多的模块',
              type: 'warning'
            })
            return
          }

        }
        if (moduleStr.match('特征选择')) {
          let preModuleText = moduleStr.substring(0, moduleStr.indexOf('特征选择'))
          if (!preModuleText.match('特征提取')) {
            ElMessage({
              showClose: true,
              message: '因模型中包含特征选择，建议在此之前包含特征提取',
              type: 'warning'
            })
            let preModule = linkedList.searchPre('特征选择')
            let sourceId = labelToId(preModule)
            let targetId = labelToId('特征选择')

            // 通过jsPlumb实例对象的select方法选择连线，并设置连线的样式
            plumbIns.select({source: sourceId, target: targetId}).setPaintStyle({
              stroke: '#E53935',
              strokeWidth: 7,
              outlineStroke: 'transparent',
              outlineWidth: 5,

            });

            return
          }
        }
        if (algorithmStr.match('深度学习模型的故障诊断') || algorithmStr.match('GRU的故障诊断') || algorithmStr.match('LSTM的故障诊断')) {
          // 如果使用深度学习的故障诊断之前有其他模块，则要进行限定

          if (moduleStr.indexOf('故障诊断') != 0) {
            let preText = moduleStr.substring(0, moduleStr.indexOf('故障诊断'))
            // 检查使用深度学习的故障诊断之前是否有特征提取等不合理的模块
            if (preText.match('特征提取') || preText.match('特征选择') || preText.match('无量纲化')) {
              ElMessage({
                showClose: true,
                message: '使用深度学习模型的故障诊断不需要进行特征提取或是特征选择，请删除相关模块！',
                type: 'warning'
              })
              return
            }

          }
        }
        if (algorithmStr.match('多传感器') && algorithmStr.match('单传感器')) {
          ElMessage({
            showClose: true,
            message: '针对单传感器的算法无法与针对多传感器的算法共用',
            type: 'warning'
          })
          return
        }
        if (moduleStr.match('无量纲化')) {
          let node
          for (let item of modeling_nodeList.value) {
            if (item.nodeInfo.label.match('无量纲化')) {
              node = item.nodeInfo
              break
            }
          }
          let useLog = node.parameters[node.use_algorithm]['useLog']  // 获取无量纲化模块的参数
          // 无量纲化处理前没有其他模块
          if (moduleStr.indexOf('无量纲化') == 0) {
            // 检查无量纲化参数设置是否合理
            if (useLog == true) {

              ElMessageBox.alert('如果要使用模型训练时使用的标准化方法进行无量纲化，请确保无量纲化模块之前对数据进行了特征提取，或者在参数设置中选择不使用模型训练时使用的标准化方法', '提示', {
                confirmButtonText: '确定',
                draggable: true,
                buttonSize: 'medium',
              })
              return
            }
          } else {

            // 检查无量纲化处理前的其他模块是否符合无量纲化的运行规则
            let preModule = moduleStr.substring(0, moduleStr.indexOf('无量纲化'))
            if (preModule.match('特征提取') && useLog == false) {
              ElMessageBox.alert(
                  '因为无量纲化模块之前已经进行了特征提取，请在无量纲化的参数设置中选择使用模型训练时使用的标准化方法进行无量纲化',
                  '提示',
                  {
                    confirmButtonText: '确定',
                    draggable: true,
                    buttonSize: 'medium',
                  }
              )
              return
            } else if (!preModule.match('特征提取') && useLog == true) {
              ElMessageBox.alert(
                  '无量纲化模块之前未进行特征提取，因此无法使用模型训练时使用的标准化方法进行无量纲化，请在无量纲化的参数设置中选择不使用模型训练时使用的标准化方法进行无量纲化',
                  '提示',
                  {
                    confirmButtonText: '确定',
                    draggable: true,
                    buttonSize: 'medium',
                  }
              )
            }
          }

        }

        // 检查模型中是否使用了深度学习模型的故障诊断
        const useDeepLearningModule = (algorithmStr: string) => {
          return algorithmStr.match('LSTM的故障诊断') || algorithmStr.match('GRU的故障诊断') || algorithmStr.match('一维卷积深度学习模型的故障诊断') || algorithmStr.match('时频图深度学习模型的故障诊断')
        }
        // 规定插值处理只能是在模型中的开始位置
        if (moduleStr.match('插值处理')) {
          if (moduleStr.indexOf('插值处理') != 0) {
            ElMessage({
              showClose: true,
              message: '插值处理只能处在模型中的开始位置',
              type: 'warning'
            })
            let preModule = linkedList.searchPre('插值处理')
            let sourceId = labelToId(preModule)
            let targetId = labelToId('插值处理')

            // 通过jsPlumb实例对象的select方法选择连线，并设置连线的样式
            plumbIns.select({source: sourceId, target: targetId}).setPaintStyle({
              stroke: '#E53935',
              strokeWidth: 7,
              outlineStroke: 'transparent',
              outlineWidth: 5,

            });
            return
          }
        }
        if (moduleStr.match('故障预测')) {
          // 故障预测之前必须进行故障诊断
          if (moduleStr.indexOf('故障预测') <= 0) {
            ElMessage({
              showClose: true,
              message: '故障预测之前需要进行故障预测',
              type: 'warning'
            })

            return
          } else {
            let preModuleText = moduleStr.substring(0, moduleStr.indexOf('故障预测'))
            if (!preModuleText.match('故障诊断')) {
              ElMessage({
                showClose: true,
                message: '故障预测之前需要进行故障诊断',
                type: 'warning'
              })
              // 将报错的连线标注为红色

              let preModule = linkedList.searchPre('故障预测')
              let sourceId = labelToId(preModule.value)
              let targetId = labelToId('故障预测')

              // 通过jsPlumb实例对象的select方法选择连线，并设置连线的样式0
              plumbIns.select({source: sourceId, target: targetId}).setPaintStyle({
                stroke: '#E53935',
                strokeWidth: 7,
                outlineStroke: 'transparent',
                outlineWidth: 5,

              });
              return
            }

          }
        }
        if (moduleStr.match('故障诊断')) {
          let useDeepLearning = useDeepLearningModule(algorithmStr)
          if (moreText(moduleStr, '故障诊断')) {
            // 机器学习的故障诊断之后只能是进行故障预测或是健康评估

            if (!useDeepLearning && !checkSubstrings(moduleStr, '故障诊断', ['层次分析模糊综合评估', '故障预测', '层次朴素贝叶斯评估', '层次逻辑回归评估', '健康评估'])) {
              ElMessage({
                showClose: true,
                message: '注意故障诊断之后仅能进行故障预测或是健康评估！',
                type: 'warning'
              })
              // 将报错的连线标注为红色
              let sourceId = labelToId('故障诊断')
              let current = linkedList.search('故障诊断')
              let next = current.next.value       // 寻找目标连线的源节点和目标节点
              let targetId = labelToId(next)

              // 通过jsPlumb实例对象的select方法选择连线，并设置连线的样式
              plumbIns.select({source: sourceId, target: targetId}).setPaintStyle({
                stroke: '#E53935',
                strokeWidth: 7,
                outlineStroke: 'transparent',
                outlineWidth: 5,

              });

              return
            }
          }
          // 如果模型中包含SVM的故障诊断，则需要先加入无量纲化操作
          if (algorithmStr.match('SVM的故障诊断')) {
            if (!moduleStr.match('无量纲化') || !checkSubstrings(moduleStr, '无量纲化', ['故障诊断'])) {
              ElMessage({
                showClose: true,
                message: '因模型中包含SVM的故障诊断，需要在此之前加入z-score标准化操作',
                type: 'warning'
              })
              // 将报错的连线标注为红色
              let sourceId = labelToId('特征选择')
              let current = linkedList.search('特征选择')
              let next = current.next.value       // 寻找目标连线的源节点和目标节点
              let targetId = labelToId(next)

              // 通过jsPlumb实例对象的select方法选择连线，并设置连线的样式
              plumbIns.select({source: sourceId, target: targetId}).setPaintStyle({
                stroke: '#E53935',
                strokeWidth: 7,
                outlineStroke: 'transparent',
                outlineWidth: 5,

              });
              return
            } else {
              if (!algorithmStr.match('z-score标准化')) {
                ElMessage({
                  showClose: true,
                  message: '因模型中包含SVM的故障诊断，需要在此之前加入z-score标准化操作',
                  type: 'warning'
                })
                return
              }
            }

          }
        }
        // 进行模型参数设置的检查
        let check_params_right = checkModelParams()
        if (check_params_right) {
          ElMessage({
            showClose: true,
            message: '模型正常，可以保存并运行',
            type: 'success'
          })
          modelCheckRight = true
          updateStatus('模型建立并已通过模型检查')
        } else {
          ElMessage({
            showClose: true,
            message: '请确保所有具有参数的模块的参数设置正确',
            type: 'warning'
          })
          return
        }
      }
    }
  } else {
    ElMessage({
      message: '请先建立模型',
      type: 'warning'
    })
    return
  }
  canSaveModel.value = false
  // canStartProcess.value = false
}

// 进度条完成度
let processing = ref(false)
let percentage = ref(0)
// let timerId = null
let fastTimerId = null; // 快速定时器ID
let slowTimerId = null; // 慢速定时器ID

let responseResults = {}  // 从后端接收到的模型运行的结果数据

const username = ref('')  // 显示在用户界面中的用户名


// 拦截器拦截axios请求，如果请求被取消，则不发送请求
// axios.interceptors.request.use(config => {
//   // 如果请求被取消，则不发送请求
//   if (config.cancelToken) {
//     config.cancelToken = source.token;
//   }
//   return config;
// });
let cancel;

const source = axios.CancelToken.source();
cancel = source.cancel; // 暴露cancel函数


//上传文件后，点击开始运行以运行程序
const startProgram = () => {

  if (!usingDatafile.value) {
    ElMessage({
      message: '请先加载数据',
      type: 'warning'
    })
    return
  }

  const data = new FormData()
  data.append("file_name", usingDatafile.value)  // 所使用的数据文件
  data.append('params', JSON.stringify(contentJson))  // 模型信息
  // console.log('params: ', contentJson)
  if (usingDatafile.value == '无') {
    ElMessage({
      message: '当前加载的数据为空，请先加载数据文件',
      type: 'error'
    })
    return
  }
  ElNotification.info({
    title: 'Waiting',
    message: '正在运行，请等待...'
  })
  canShutdown.value = false

  percentage.value = 0; // 重置进度条

  fastTimerId = setInterval(() => {
    if (percentage.value < 50) {
      percentage.value += 10;
    } else {
      // 达到50%时，清除快速定时器并启动慢速定时器
      clearInterval(fastTimerId);
      slowTimerId = setInterval(() => {
        if (percentage.value < 90) {
          percentage.value += 10;
        } else {
          // 达到100%时清除慢速定时器
          clearInterval(slowTimerId);
        }
      }, 3000);
    }
  }, 1000);

  // 显示进度条
  resultsViewClear()
  processing.value = true
  showStatusMessage.value = false
  showPlainIntroduction.value = false

  api.post('user/run_with_datafile_on_cloud/', data,
      {
        headers: {"Content-Type": 'multipart/form-data'},
        cancelToken: source.token, // 将cancelToken传递给axios
      }
  ).then((response) => {
    if (response.data.code == 401) {
      ElMessageBox.alert('登录状态已失效，请重新登陆', '提示', {
        confirmButtonText: '确定',
        callback: (action: Action) => {
          router.push('/')
        },
      })
    }
    if (response.data.code === 200) {

      if (!processIsShutdown.value) {
        ElNotification.success({
          title: 'Success',
          message: '程序运行完成',
        })
        responseResults = response.data.results
        missionComplete.value = true
        statusMessageToShow.value = statusMessage.success

      } else {
        processIsShutdown.value = false
      }
    } else if (response.data.code == 404) {
      statusMessageToShow.value = statusMessage.error
      ElMessage({
        message: response.data.message,
        type: 'warning'
      })
    }
    clearInterval(fastTimerId);
    clearInterval(slowTimerId);
    setTimeout(function () {
      processing.value = false
    }, 700)
    percentage.value = 100;
    canShutdown.value = true

    resultsViewClear()

    showStatusMessage.value = true
    showPlainIntroduction.value = false
  })
      .catch(error => {

        if (error.response) {
          // 请求已发出，服务器响应了状态码，但不在2xx范围内
          console.log(error.response.status); // HTTP状态码
          console.log(error.response.statusText); // 状态消息

        } else if (error.request) {
          // 请求已发起，但没有收到响应
          console.log(error.request);
        } else {
          // 设置请求时触发了错误
          console.error('Error', error.message);
        }

        ElNotification.error({
          title: 'Error',
          message: '运行出错，' + error.response.data?.message,
        })
        loading.value = false
        processing.value = false

        canShutdown.value = true
        statusMessageToShow.value = statusMessage.error
        resultsViewClear()
        showStatusMessage.value = true
        missionComplete.value = false

      })
}

// 用于判断该程序是否是正常运行结束的，如果该变量为真，表示为手动终止运行
const processIsShutdown = ref(false)


// 终止模型的运行
const shutDown = () => {
  api.get('/shut').then((response: any) => {
    if (response.data.status == 'shutdown' && processing.value == true) {
      loading.value = false
      processing.value = false
      missionComplete.value = false
      ElNotification.info({
        title: 'INFO',
        message: '进程已终止'
      })
      resultsViewClear()
      processIsShutdown.value = true
      statusMessageToShow.value = statusMessage.shutdown
      showStatusMessage.value = true
      canShutdown.value = true
      // canStartProcess.value = false
      // cancel('Operation canceled by the user.');
    }
  }).catch(function (error: any) {
    // 处理错误情况
    ElNotification.error({
      title: 'ERROR',
      message: '请求终端进程失败'
    })
    console.log('请求中断进程失败：' + error)
  });
}


const isShow = ref(false)
const selects = ref(false)

const efContainerRef = ref()
const nodeRef = ref([])

const nodeList = ref([])   // 保存可视化建模区中的各节点的列表

// 前端向后端传递的要运行的模型的信息，由包括的模块、模块使用的算法、使用的参数、模块的运行顺序组成
const contentJson = {
  'modules': [],
  'algorithms': {},
  'parameters': {},
  'schedule': [],
  'multipleSensor': false  // 是否为多传感器数据
}

let plumbIns   // 实例化的jsPlumb对象，实现用户建模的连线操作
let missionComplete = ref(false)
let loading = ref(false)
let modelSetup = ref(false)

// 清除页面中的内容，包括使用的模型、文件和算法介绍等信息
const handleClear = () => {
  done.value = false
  nodeList.value = []  // 可视化建模区的节点列表
  // features.value = []  // 特征提取选择的特征
  // features.value = ['均值', '方差', '标准差', '峰度', '偏度', '四阶累积量', '六阶累积量', '最大值', '最小值', '中位数', '峰峰值', '整流平均值', '均方根', '方根幅值',
  //   '波形因子', '峰值因子', '脉冲因子', '裕度因子', '重心频率', '均方频率', '均方根频率', '频率方差', '频率标准差', '谱峭度的均值', '谱峭度的标准差', '谱峭度的峰度', '谱峭度的偏度']
  jsonClear()    // 向后端发送的模型信息
  isShow.value = false
  // plumbIns.deleteEveryConnection()
  // plumbIns.deleteEveryEndpoint()
  // linkedList.head = null
  // linkedList.tail = null
  missionComplete.value = false // 程序处理完成
  modelSetup.value = false   // 模型设置完成
  showPlainIntroduction.value = false
  showStatusMessage.value = false
  modelHasBeenSaved = false  //复用历史模型，不做模型检查
  toRectifyModel.value = false  // 禁用修改模型
  // canCompleteModeling.value = true
  canCheckModel.value = true
  canSaveModel.value = true
  processIsShutdown.value = false
  canStartProcess.value = true   // 不可运行程序
  modelLoaded.value = '无'

  updateStatus('未建立模型')

  resultsViewClear()
}

// 用于清空向后端传递的要运行的模型的信息
const jsonClear = () => {
  contentJson.modules = []
  contentJson.algorithms = {}
  contentJson.parameters = {}
  contentJson.schedule = []
}
const jsPlumbInit = () => {
  plumbIns.importDefaults(deff.jsplumbSetting)
}

// 数据源节点的节点信息
const dataSourceNode = {id: '4', label: '数据源', parameters: {dataSource: {}}, optional: true}

// 自定义模块节点的节点信息
const customModuleNode = {id: '5', label: '自定义模块', parameters: {customModule: {}}, optional: true}

//处理拖拽，初始化节点的可连接状态
const handleDragend = (ev, algorithm, node) => {

  // 拖拽进来相对于地址栏偏移量
  const evClientX = ev.clientX
  const evClientY = ev.clientY
  let left
  if (evClientX < 300) {
    left = evClientX + 'px'
  } else {
    left = evClientX - 300 + 'px'
  }

  let top = 50 + 'px'
  const nodeId = node.id
  const nodeInfo = {
    label_display: labelsForAlgorithms[algorithm],   // 具体算法的名称
    label: node.label,      // 算法模块名称
    id: node.id,
    nodeId,
    nodeContainerStyle: {
      left: left,
      top: top,
    },
    use_algorithm: algorithm,
    parameters: node.parameters,
    optional: node.optional
  }

  // 针对时域或是频域特征给出不同的可选特征
  if (nodeInfo.label_display.indexOf('时域和频域') > -1) {
    features.value = ['均值', '方差', '标准差', '峰度', '偏度', '四阶累积量', '六阶累积量', '最大值', '最小值', '中位数', '峰峰值', '整流平均值', '均方根', '方根幅值',
      '波形因子', '峰值因子', '脉冲因子', '裕度因子', '重心频率', '均方频率', '均方根频率', '频率方差', '频率标准差', '谱峭度的均值', '谱峭度的峰度']
  } else {
    if (nodeInfo.label_display.indexOf('时域特征') > -1) {
      features.value = ['均值', '方差', '标准差', '峰度', '偏度', '四阶累积量', '六阶累积量', '最大值', '最小值', '中位数', '峰峰值', '整流平均值', '均方根', '方根幅值',
        '波形因子', '峰值因子', '脉冲因子', '裕度因子']
    } else if (nodeInfo.label_display.indexOf('频域特征') > -1) {
      features.value = ['重心频率', '均方频率', '均方根频率', '频率方差', '频率标准差', '谱峭度的均值', '谱峭度的峰度']
    }
  }
  // console.log(nodeInfo)
  //算法模块不允许重复
  if (nodeList.value.length === 0) {
    nodeList.value.push(nodeInfo)
  } else {
    let isDuplicate = false;
    for (let i = 0; i < nodeList.value.length; i++) {
      let nod = nodeList.value[i];
      if (nod.id == node.id) {
        // window.alert('不允许出现重复模块');
        ElMessage({
          message: '不允许出现同一类别的算法',
          type: 'warning'
        })
        isDuplicate = true;
        break;
      }
    }
    // 向节点列表中添加新拖拽入可视化建模区中的模块
    if (!isDuplicate) {
      nodeList.value.push(nodeInfo);
    }
  }

  // 将节点初始化为可以连线的状态
  nextTick(() => {
    plumbIns.draggable(nodeId, {containment: "efContainer"})

    if (node.id < 4) {
      plumbIns.makeSource(nodeId, deff.jsplumbSourceOptions)
    }

    if (node.id == '4') {
      plumbIns.makeSource(nodeId, deff.jsplumbSourceOptions)
      return
    }

    plumbIns.makeTarget(nodeId, deff.jsplumbTargetOptions)

  })
}

// 删除节点
const deleteNode = (nodeId) => {
  if (!modelSetup.value) {
    nodeList.value = nodeList.value.filter(node => node.id !== nodeId);
    plumbIns.deleteEveryConnection()
    plumbIns.deleteEveryEndpoint()
    linkedList.head = null
    linkedList.tail = null
    canCheckModel.value = true
    canStartProcess.value = true
    canShutdown.value = true
    canSaveModel.value = true
  }
}

// 处理可视化建模区中拖拽节点的操作
const handleMouseup = (ev, data) => { // 在图表中拖拽节点时，设置他的新的位置

  if (!done.value) {
    length = nodeList.value.length
    for (let i = 0; i < length; i++) {
      let node = nodeList.value[i]
      if (node.id === data.id) {
        // setTimeout(()=>{
        //   data.nodeContainerStyle.left = ev.clientX - 290
        //   data.nodeContainerStyle.top = ev.clientY - 80
        // }, 2)
        nodeList.value[i].nodeContainerStyle.left = ev.clientX - 355 + 'px'
        nodeList.value[i].nodeContainerStyle.top = ev.clientY - 105 + 'px'
      }
    }
  }

}

// const modelsetting = () => {
//   selects.value = !selects.value
// }

const dialogFormVisible = ref(false)  // 控制保存模型对话框的弹出，输入要保存的模型的名称

// 提交的模型相关信息
const modelInfoForm = ref({
  name: '',
  description: '',
  class: null
})

// 检查模型参数设置
const checkModelParams = () => {
  for (let i = 0; i < nodeList.value.length; i++) {
    let dict = nodeList.value[i]
    console.log('dict.use_algorithm: ', dict.use_algorithm)
    if (!dict.use_algorithm) {
      return false
    } else {
      // 检查特征选择的规则参数
      if (dict.id == '1.3') {
        let threshold = false
        // 检查选择特征的规则参数是否正确设置
        let rule = dict.parameters[dict.use_algorithm].rule
        if (dict.parameters[dict.use_algorithm]['threshold' + rule]) {
          threshold = true
        }
        if (!threshold) {
          return false
        }
      } else if (dict.id == '1.2') {
        // 检查特征提取参数设置
        if (!features.value.length) {
          return false
        }
      } else if(dict.id == '1.4'){
           console.log('检测到小波变换，单独赋值: ', dict.parameters)
      } else {
        console.log('dict信息: ', dict)
        console.log('dict.use: ', dict.use_algorithm)
        console.log('dict.parameters: ', dict.parameters)
        // 检查一般算法模块的参数设置，参数设置不能为空
        let parameters = dict.parameters[dict.use_algorithm]
        console.log('parameters: ', parameters)
        if (!parameters) {
          console.log('parameters is null')
          return false
        } else {
          for (let key in parameters) {
            console.log("parameters", parameters[key])
            console.log("key....", key)
            if (parameters[key] === '' || parameters[key] === null) {
              console.log('parameters[key] is null: ', parameters[key])
              return false
            }
          }
        }
      }
    }
  }

  return true
}

//保存模型，并取消拖拽动作
const saveModelSetting = (saveModel, schedule) => {

  done.value = true

  // dialogFormVisible.value = true
  // selects.value = !selects.value
  jsonClear()
  for (let i = 0; i < nodeList.value.length; i++) {
    let dict = nodeList.value[i]

    if (!dict.use_algorithm) {
      ElMessage({
        message: '请设置每个算法的必选属性',
        type: 'error'
      })

      return
    }

    contentJson.algorithms[dict.label] = dict.use_algorithm
    if (!contentJson.modules.includes(dict.label) && dict.id !== '4') {
      contentJson.modules.push(dict.label);
    }

    // 选择特征提取需要提取的参数
    if (dict.id == '1.2') {
      let params = dict.parameters[dict.use_algorithm]
      if (!features.value.length) {
        ElMessage({
          message: '请设置每个算法的必选属性',
          type: 'error'
        })
        return
      }
      features.value.forEach(element => {
        if (params[element] == false) {
          params[element] = true
        }
      });
      contentJson.parameters[dict.use_algorithm] = params
      continue
    }
    contentJson.parameters[dict.use_algorithm] = dict.parameters[dict.use_algorithm]
    // console.log(dict.use_algorithm + '\'s params are: ' + dict.parameters[dict.use_algorithm])

  }
  if (!modelCheckRight && saveModel) {
    ElMessage({
      message: '请先建立模型并通过模型检查！',
      type: 'warning'
    })
    return
  }

  contentJson.schedule.length = 0

  if (!saveModel) {
    // 如果是加载的已保存的模型，则直接使用已保存模型的流程
    // console.log('schedule: ', schedule)
    contentJson.schedule = schedule
    // console.log('content_json: ', contentJson)
  } else {
    let current = linkedList.head;
    if (!current) {
      ElNotification({
        title: 'WARNING',
        message: '未建立流程，请先建立流程',
        type: 'warning',
      })
      return
    }
    // 使用自定义模型链表建立的流程
    while (current) {
      // if (current.value == '数据源') continue

      contentJson.schedule.push(current.value);
      current = current.next;
    }
  }

  dialogModle.value = saveModel
}

//检查保存模型的表单
const checkForm = () => {
  if ((modelInfoForm.value.name === '')  |  (modelInfoForm.value.class.length==0)  | (modelInfoForm.value.description=='')) {
    return false
  }else{
    return true
  }
}

// 返回筛选后的树形结构
const filteredDataSource = computed(() => {
  return filterTreeData(dataSourceOfTree)
})

const filterTreeData = (data) => {
  return data.filter(item => {
    if (item.isModel) return false;
    if (item.children) {
      item.children = filterTreeData(item.children);
    }
    return true;
  });
}

// 用于控制模型树子组件
const superComponentTree = ref()
// 完成模型名称等信息的填写后，确定保存模型
const saveModelConfirm = async (formEl: FormInstance | undefined) => {
  if(contentJson.schedule.length==0){
    ElMessage({
      message: '请先建立并检查模型',
      type: 'warning'
    })
    return
  }else{
    if(!checkForm()){
      ElMessage({
        message: '请填写完整信息',
        type: 'warning'
      })
      return
    }else{

      console.log('saveModelConfirm modelInfoForm: ', modelInfoForm.value)
      // 将模型信息保存到数据库
      let data = new FormData()
      data.append('model_name', modelInfoForm.value.name)
      let nodelistInfo = toObject()
      let modelInfo = {"nodeList": nodelistInfo, "connection": contentJson.schedule}
      data.append('model_info', JSON.stringify(modelInfo))
      data.append('description', modelInfoForm.value.description)

      let treeName = modelInfoForm.value.class.split('.')[0]  // 根节点（树名）
      let parentNodeValue = modelInfoForm.value.class  // 所属于类型的节点值

      console.log('saveModelConfirm treeName: ', treeName)
      console.log('saveModelConfirm parentNodeValue: ', parentNodeValue)
      data.append('treeName', treeName)
      data.append('parentNode', parentNodeValue)

      // 获取树名和节点值

      api.post('/user/save_model/', data,
          {
            headers: {"Content-Type": 'multipart/form-data'}
          }
      ).then((response: any) => {
        if (response.data.code == 401) {
          ElMessageBox.alert('登录状态已失效，请重新登陆', '提示', {
            confirmButtonText: '确定',
            callback: (action: Action) => {
              router.push('/')
            },
          })
        }
        if (response.data.code == 200) {
          ElMessage({
            message: '保存模型成功',
            type: 'success'
          })
          // 刷新模型结构树以及模型列表
          superComponentTree.value.getComponentTrees()
          superComponentTree.value.fetchModelInfoFromDatabase()
          getComponentTrees();

          modelsDrawer.value = true       // 关闭历史模型抽屉
          dialogFormVisible.value = false    // 关闭提示窗口
          dialogModle.value = false
          canStartProcess.value = false     // 保存模型成功可以运行
          modelSetup.value = true                 // 模型保存完成
          modelLoaded.value = modelInfoForm.value.name  // 保存模型后，显示当前模型名称
          updateStatus('当前模型已保存')
        } else if (response.data.code == 400) {
          ElMessage({
            message: '已有同名模型，保存模型失败',
            type: 'error'
          })
        } else {
          ElMessage({
            message: '保存模型失败，'+ response.data.message,
            type: 'error'
          })
        }
      }).catch(error => {
        ElMessage({
          message: '保存模型请求失败',
          type: 'error'
        })
        console.log('save model error: ', error)
      })
    }
  }

}

const showResultSs = ref('')

const show1 = ref(false)

// 结果可视化区域显示
const canShowResults = ref(false)

// 健康评估结果展示
const healthEvaluation = ref('')
const displayHealthEvaluation = ref(false)
const generateHealthEvaluationFigure = ref(false)
const activeName1 = ref('first')
const healthEvaluationOfExample = ref('样本1')
const resultsBarOfAllExamples = ref({});
const levelIndicatorsOfAllExamples = ref({});
const statusOfExamples = ref({});
const suggestionOfAllExamples = ref({});
const finalSuggestion = ref('');
// const healthEvaluationFigure1 = ref('data:image/png;base64,')
// const healthEvaluationFigure2 = ref('data:image/png;base64,')
// const healthEvaluationFigure3 = ref('data:image/png;base64,')

// const healthEvaluationDisplay = (results_object) => {

//   // 各个样本健康评估的可视化结果
//   displayHealthEvaluation.value = true

//   let figure1 = results_object.层级有效指标_Base64
//   let figure2 = results_object.二级指标权重柱状图_Base64
//   let figure3 = results_object.评估结果柱状图_Base64
//   let suggestions = results_object.评估建议

//   figure1.forEach((element: string, index: number) => {
//     // console.log("element: ", element)
//     // console.log("index: ", index)
//     resultsBarOfAllExamples.value[`样本${index + 1}`] = 'data:image/png;base64,' + element
//   });
//   figure2.forEach((element: string, index: number) => {
//     levelIndicatorsOfAllExamples.value[`样本${index + 1}`] = 'data:image/png;base64,' + element
//   });
//   figure3.forEach((element: string, index: number) => {
//     statusOfExamples.value[`样本${index + 1}`] = 'data:image/png;base64,' + element
//   });
//   suggestions.forEach((element: string, index: number) => {
//     suggestionOfAllExamples.value[`样本${index + 1}`] = element
//   });

//   // 最终评估结果
//   finalSuggestion.value = results_object.最终评估结果
//   let statusOfAllExamples: Object = results_object.各样本状态隶属度

//   nextTick(() => {
//     // 绘制故障样本与非故障样本数量饼状图
//     var pieChartDom = document.getElementById('healthEvaluationPieChart');
//     var pieChart = echarts.init(pieChartDom);
//     var pieChartOption;

//     pieChartOption = {
//       title: {
//         text: '评估结果中不同状态所属的样本数量比例',
//         // subtext: 'Fake Data',
//         left: 'center'
//       },
//       tooltip: {
//         trigger: 'item'
//       },
//       legend: {
//         orient: 'vertical',
//         left: 'left'
//       },
//       series: [
//         {
//           name: '样本数量',
//           type: 'pie',
//           radius: '50%',
//           data: [
//             // { value: 580, name: 'Email' },
//             // { value: 484, name: 'Union Ads' },
//             // { value: 300, name: 'Video Ads' }
//           ],
//           emphasis: {
//             itemStyle: {
//               shadowBlur: 10,
//               shadowOffsetX: 0,
//               shadowColor: 'rgba(0, 0, 0, 0.5)'
//             }
//           }
//         }
//       ],
//       dataZoom: [
//         {
//           type: 'inside', // 使用鼠标滚轮来缩放
//           start: 0,
//           end: 100,
//         },/*
//         {
//           show: true,
//           type: 'slider', // 在图表下方显示滑动条
//           start: 0,
//           end: 100,
//         },*/
//       ],
//     };
//     for (let [key, value] of Object.entries(statusOfAllExamples)) {
//       pieChartOption.series[0].data.push({value: value, name: key})
//     }
//     console.log("pieChartOption.series[0].data: ", pieChartOption.series[0].data)
//     pieChart.setOption(pieChartOption);
//   })
//   // healthEvaluation.value = results_object.评估建议
//   // healthEvaluationFigure1.value = 'data:image/png;base64,' + figure1
//   // healthEvaluationFigure2.value = 'data:image/png;base64,' + figure2
//   // healthEvaluationFigure3.value = 'data:image/png;base64,' + figure3

// }

const healthEvaluationDisplay = async(results_object: any) => {

// 各个样本健康评估的可视化结果
// displayHealthEvaluation.value = true

let figure1 = results_object.层级有效指标_Base64
let figure2 = results_object.二级指标权重柱状图_Base64
let figure3 = results_object.评估结果柱状图_Base64
let suggestions = results_object.评估建议

// 显示各个样本健康评估的可视化结果
resultsBarOfAllExamples.value = {}
figure1.forEach((element: string, index: number) => {
  // console.log("element: ", element)
  // console.log("index: ", index)
  resultsBarOfAllExamples.value[`样本${index + 1}`] = 'data:image/png;base64,' + element
});
levelIndicatorsOfAllExamples.value = {}
figure2.forEach((element: string, index: number) => {
  levelIndicatorsOfAllExamples.value[`样本${index + 1}`] = 'data:image/png;base64,' + element
});
statusOfExamples.value = {};
figure3.forEach((element: string, index: number) => {
  statusOfExamples.value[`样本${index + 1}`] = 'data:image/png;base64,' + element
});
suggestionOfAllExamples.value = {};
suggestions.forEach((element: string, index: number) => {
  suggestionOfAllExamples.value[`样本${index + 1}`] = element
});

// 最终评估结果
finalSuggestion.value = results_object.最终评估结果
resultsToGenerateConclusion['healthEvaluation']['text'] = finalSuggestion.value
let statusOfAllExamples: Object = results_object.各样本状态隶属度

nextTick(() => {
  // 绘制故障样本与非故障样本数量饼状图
  var pieChartDom = document.getElementById('healthEvaluationPieChart');
  let existingChart = echarts.getInstanceByDom(pieChartDom);

  if(!existingChart){

    var pieChart = echarts.init(pieChartDom);
    var pieChartOption;

    pieChartOption = {
      animation: false,
      title: {
        text: '评估结果中不同状态所属的样本数量比例',
        // subtext: 'Fake Data',
        left: 'center'
      },
      tooltip: {
        trigger: 'item'
      },
      legend: {
        orient: 'vertical',
        left: 'left'
      },
      series: [
        {
          name: '样本数量',
          type: 'pie',
          radius: '50%',
          data: [
            // { value: 580, name: 'Email' },
            // { value: 484, name: 'Union Ads' },
            // { value: 300, name: 'Video Ads' }
          ],
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }
      ]
    };
    for (let [key, value] of Object.entries(statusOfAllExamples)) {
      pieChartOption.series[0].data.push({value: value, name: key})
    }
    // console.log("pieChartOption.series[0].data: ", pieChartOption.series[0].data)
    pieChart.setOption(pieChartOption);

    // 将echart以Base64图像编码的形式存放到resultPicturesToGenerateConclusion中
    var imgSrc = pieChart.getDataURL({
        type: 'png',  // 可选 'jpeg'
        backgroundColor: '#fff',
        excludeComponents: ['toolbox']
    });
    // 去除图片Base64编码前缀
    imgSrc = imgSrc.replace(/^data:image\/[a-z]+;base64,/, "");

    // 向最终报告添加健康评估的结果
    resultsToGenerateConclusion['healthEvaluation']['imageBase64'] = imgSrc
    resultsToGenerateConclusion['healthEvaluation']['text'] = finalSuggestion.value
  }

})
// healthEvaluation.value = results_object.评估建议
// healthEvaluationFigure1.value = 'data:image/png;base64,' + figure1
// healthEvaluationFigure2.value = 'data:image/png;base64,' + figure2
// healthEvaluationFigure3.value = 'data:image/png;base64,' + figure3

}


// 特征提取结果展示
const displayFeatureExtraction = ref(false)
const generateFeatureExtractionFigure = ref(false)
// const transformedData = ref([])
// const columns = ref([])
const numOfSensors = ref<number>(0)
const rawDataList = ref<Object[]>([])
const featuresSeriesList = ref<Object[]>([])
const featuresExtractionRawData = ref('传感器 1')

const featureExtractionDisplay = async(resultsObject: any) => {


// 获取后端传回的提取的特征
let featuresWithName = Object.assign({}, resultsObject.features_with_name)
let featuresName = featuresWithName.features_name
let featuresToDrawLineChart = Object.assign({}, resultsObject.featuresToDrawLineChart)
// let featuresGroupBySensor = Object.assign(featuresWithName.features_extracted_group_by_sensor)

console.log("featuresToDrawLineChart: ", featuresToDrawLineChart)

let num_frames = resultsObject.num_examples
// 根据帧数num_frames生成x坐标的坐标轴
let x_axis = []
for (let i = 0; i < num_frames; i++) {
  x_axis.push('样本' + (i + 1) + `(${i * 2048}~${(i + 1) * 2048 - 1})`)
}

let rawDataSeries: any = resultsObject.raw_data
numOfSensors.value = rawDataSeries.length
console.log('rawDataSeries: ', rawDataSeries)
// 原始信号波形图显示
let sensorNo = 1
rawDataList.value.length = 0
for (let series of rawDataSeries) {
  rawDataList.value.push({
    'sensor_no': '传感器 ' + sensorNo,
    'data': series,
  })
  sensorNo += 1
}
sensorNo = 1
featuresSeriesList.value.length = 0
for (let features of Object.values(featuresToDrawLineChart)) {
  featuresSeriesList.value.push({
    'sensor_no': '传感器 ' + sensorNo,
    'data': features,
  })
  sensorNo += 1
}
// console.log('featuresSeriesList: ', featuresSeriesList.value)
featuresExtractionRawData.value = rawDataList.value[0].sensor_no  //默认显示第一个传感器的原始信号

// displayFeatureExtraction.value = true  // 显示特征提取结果

// console.log('length: ', num_sensors.value)
nextTick(() => {
  // 使用echarts绘制特征提取的原始信号波形图
  rawDataList.value.forEach(object => {
    let domElement = document.getElementById(object.sensor_no);
    let existingChart = echarts.getInstanceByDom(domElement);
    if(!existingChart){
      let chart = echarts.init(domElement)
      let dataSeries = object.data
      let option = {
        animation: false,
        title: {
          text: '原始信号'
        },
        xAxis: {
          type: 'value',
          data: Array.from({length: dataSeries.length}),
          name: '采样点'
        },
        yAxis: {
          type: 'value',
          name: '采样值'
        },
        series: [
          {
            name: '信号',
            type: 'line',
            symbol: 'circle',
            symbolSize: 2,
            data: dataSeries.map((value, index) => [index, value]),
          }
        ]
      }
      chart.setOption(option)
    }
    
  })
  featuresSeriesList.value.forEach(object => {
    // 使用echarts绘制特征提取的特征折线图
    type EChartsOption = echarts.EChartsOption;
    let domElement = document.getElementById(object.sensor_no + 'features');
    let existingChart = echarts.getInstanceByDom(domElement);

    if (!existingChart){
      let dataSeries = object.data
      var lineChart = echarts.init(domElement);
      var lineChartOption: EChartsOption;

      lineChartOption = {
        animation: false,
        title: {
          text: '连续信号样本提取特征'
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          // data: ['Email', 'Union Ads', 'Video Ads', 'Direct', 'Search Engine']
          left: 'center',
          top: '5%',
          bottom: '6%',
          data: featuresName
        },
        grid: {
          left: '5%',
          right: '5%',
          bottom: '3%',
          containLabel: true
        },
        toolbox: {
          feature: {
            saveAsImage: {}
          }
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          // data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
          data: x_axis
        },
        yAxis: {
          type: 'value'
        },
        series: []
      };
      for (let key of featuresName) {
        lineChartOption.series.push({
          name: key,
          type: 'line',
          stack: 'Total',
          data: dataSeries[key]
        })
      }
      lineChart.setOption(lineChartOption)
      var imgSrc = lineChart.getDataURL({
        type: 'jpeg',  // 可选 'jpeg'
        backgroundColor: '#fff',
        excludeComponents: ['toolbox']
      });
      // 提取 Base64 编码部分
      var base64Image = imgSrc.split(',')[1];
      // console.log(" feature extraction base64Image: ", base64Image)
      // 将imgsrc编码为字符串
      resultsToGenerateConclusion['featureExtraction']['imageBase64'] = base64Image
    }
  })
  resultsToGenerateConclusion['featureExtraction']['text'] = '对输入信号特征提取结果如下'
})
}






// 特征选择结果可视化
const displayFeatureSelection = ref(false)
const generateFeatureSelectionFigure = ref(false)
const featureSelectionFigure = ref('')
const featuresSelected = ref('')
const selectFeatureRule = ref('')
const correlationFigure = ref('')
const featuresSelectionTabs = ref('first')

// const featuresSelectionDisplay = (resultsObject) => {
//   displayFeatureSelection.value = true

//   let figure1 = resultsObject.figure_Base64
//   let figure2 = resultsObject.heatmap_Base64
//   featuresSelected.value = resultsObject.selected_features.join('、')

//   selectFeatureRule.value = resultsObject.rule
//   featureSelectionFigure.value = 'data:image/png;base64,' + figure1
//   correlationFigure.value = 'data:image/png;base64,' + figure2

// }


const featuresSelectionDisplay = async(resultsObject: any) => {
  // displayFeatureSelection.value = true

  let figure1 = resultsObject.figure_Base64
  let figure2 = resultsObject.heatmap_Base64
  featuresSelected.value = resultsObject.selected_features.join('、')

  selectFeatureRule.value = resultsObject.rule
  featureSelectionFigure.value = 'data:image/png;base64,' + figure1
  correlationFigure.value = 'data:image/png;base64,' + figure2

  resultsToGenerateConclusion['featureSelection']['imageBase64'] = figure1
  resultsToGenerateConclusion['featureSelection']['text'] = '对输入信号进行特征选择后，最终选择的特征为' + featuresSelected.value
  // 将 Base64 字符串转换为二进制数组
  // const binaryData = base64ToArrayBuffer(figure1);
  

}





// 用户对于故障诊断结果准确性的反馈
const feedBackDialogVisible = ref(false)
// const feedbackContent = ref('')
const feedBackFormRef = ref()

const feedBackRules = {
  module: [
    { required: true, message: '请选择一个模块', trigger: 'change' }
  ],
  feedbackContent: [
    { required: true, message: '请输入问题描述', trigger: 'blur' },
    { pattern: /^[\u4e00-\u9fa5a-zA-Z0-9_]+$/, message: '只能包含中英文字符、数字和下划线', trigger: 'blur' }
  ]
}


const feedBackFormRefState = reactive({
  module: '',
  feedbackContent: ''
})

const feedBack = () => {
  // console.log("feedBackFormRef: ", feedBackFormRef.value)
  feedBackFormRef.value.validate().then(() => {
    
    const formData = new FormData();
    formData.append('username', username.value)
    formData.append('datafile', usingDatafile.value)
    // console.log("feedBack modelLoaded: ", modelLoaded.value)
    formData.append('modelName', modelLoadedName.value)
    formData.append('module', feedBackFormRefState.module)
    formData.append('question', feedBackFormRefState.feedbackContent)
    formData.append('modelId', modelLoadedId)
    api.post('user/user_feedback/', formData).then((response: any)=>{
        if(response.data.code === 200){

          message.success('已收到您的反馈')
        }else{
          message.error("反馈提交失败, ", response.data.message)
        }
      }
    )
    .catch((error: any) => {
      console.log("上传反馈失败", error)
      message.error("上传反馈失败")
    })
  })
  .catch((error: any) => {
    console.error('反馈提交失败', error);
  })
}



// 故障诊断结果展示
const displayFaultDiagnosis = ref(false)
const generateFaultDiagnosisFigure = ref(false)
const faultDiagnosis = ref('')
const faultDiagnosisFigure = ref('')  // 原始信号波形图
const faultDiagnosisComplementaryFigure = ref('')  // 补充的故障诊断结果图
const faultDiagnosisComplementarySummary = ref('')  // 补充的故障诊断结果总结
const faultDiagnosisResultsText = ref('')
const faultDiagnosisResultOption = ref('2')

// const faultDiagnosisDisplay = (resultsObject: any) => {
//   displayFaultDiagnosis.value = true

//   let figure1 = resultsObject.figure_Base64
//   let diagnosisResult = resultsObject.diagnosis_result
//   let indicator = resultsObject.indicator
//   let x_axis = resultsObject.x_axis
//   let num_has_fault = resultsObject.num_has_fault
//   let num_has_no_fault = resultsObject.num_has_no_fault

//   console.log('indicator: ', indicator)
//   // 获取indicator的key
//   let indicatorKeys = Object.keys(indicator)

//   nextTick(() => {

//     // 绘制连续样本指标变化折线图
//     type EChartsOption = echarts.EChartsOption;
//     var lineChartDom = document.getElementById('indicatorVaryingFigure')!;
//     var lineChart = echarts.init(lineChartDom);
//     var lineChartOption: EChartsOption;

//     lineChartOption = {
//       title: {
//         text: '连续样本指标变化曲线图'
//       },
//       tooltip: {
//         trigger: 'axis'
//       },
//       legend: {
//         // data: ['Email', 'Union Ads', 'Video Ads', 'Direct', 'Search Engine']
//         left: 'center',
//         top: '5%',
//         bottom: '6%',
//         data: indicatorKeys
//       },
//       grid: {
//         left: '5%',
//         right: '5%',
//         bottom: '3%',
//         containLabel: true
//       },
//       toolbox: {
//         feature: {
//           saveAsImage: {}
//         }
//       },
//       xAxis: {
//         type: 'category',
//         boundaryGap: false,
//         // data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
//         data: x_axis
//       },
//       yAxis: {
//         type: 'value'
//       },
//       series: [],
//       dataZoom: [
//         {
//           type: 'inside', // 使用鼠标滚轮来缩放
//           start: 0,
//           end: 100,
//         },/*
//         {
//           show: true,
//           type: 'slider', // 在图表下方显示滑动条
//           start: 0,
//           end: 100,
//         },*/
//       ],
//     };

//     for (let key in indicator) {
//       lineChartOption.series.push({
//         name: key,
//         type: 'line',
//         stack: 'Total',
//         data: indicator[key]
//       })
//     }
//     lineChart.setOption(lineChartOption);

//     // 绘制故障样本与非故障样本数量饼状图
//     var pieChartDom = document.getElementById('faultExampleRatioFigure');
//     var pieChart = echarts.init(pieChartDom);
//     var pieChartOption;

//     pieChartOption = {
//       title: {
//         text: '预测结果中不同类型样本数量比例',
//         // subtext: 'Fake Data',
//         left: 'center'
//       },
//       tooltip: {
//         trigger: 'item'
//       },
//       legend: {
//         orient: 'vertical',
//         left: 'left'
//       },
//       series: [
//         {
//           name: '样本数量',
//           type: 'pie',
//           radius: '50%',
//           data: [
//             {value: num_has_fault, name: '预测为故障类型的样本'},
//             {value: num_has_no_fault, name: '预测为非故障类型的样本'},
//             // { value: 580, name: 'Email' },
//             // { value: 484, name: 'Union Ads' },
//             // { value: 300, name: 'Video Ads' }
//           ],
//           emphasis: {
//             itemStyle: {
//               shadowBlur: 10,
//               shadowOffsetX: 0,
//               shadowColor: 'rgba(0, 0, 0, 0.5)'
//             }
//           }
//         }
//       ],
//       dataZoom: [
//         {
//           type: 'inside', // 使用鼠标滚轮来缩放
//           start: 0,
//           end: 100,
//         },/*
//         {
//           show: true,
//           type: 'slider', // 在图表下方显示滑动条
//           start: 0,
//           end: 100,
//         },*/
//       ],
//     };

//     pieChart.setOption(pieChartOption);
//   })


//   faultDiagnosisResultsText.value = resultsObject.resultText
//   if (diagnosisResult == 0) {
//     faultDiagnosis.value = '无故障'
//   } else {
//     faultDiagnosis.value = '存在故障'
//   }
//   faultDiagnosisFigure.value = 'data:image/png;base64,' + figure1

// }


const canShowIndicator = ref(false)

const faultDiagnosisDisplay = async(resultsObject: any) => {
  // displayFaultDiagnosis.value = true

  let figure1 = resultsObject.figure_Base64
  let diagnosisResult = resultsObject.diagnosis_result
  let indicator = resultsObject.indicator
  let x_axis = resultsObject.x_axis
  let num_has_fault = resultsObject.num_has_fault
  let num_has_no_fault = resultsObject.num_has_no_fault

  console.log('num_has_fault: ', num_has_fault)
  console.log('num_has_no_fault: ', num_has_no_fault)
  console.log('indicator: ', indicator)

  if (indicator != 'none'){
    canShowIndicator.value = true
  }

  console.log('indicator: ', indicator)
  // 获取indicator的key
  let indicatorKeys = Object.keys(indicator)

  nextTick(() => {

    // 绘制连续样本指标变化折线图

    if (indicator != 'none'){
      
      type EChartsOption = echarts.EChartsOption;

      let lineChartDom = document.getElementById('indicatorVaryingFigure')
      let existingLineChart = echarts.getInstanceByDom(lineChartDom);

      if(!existingLineChart){
        var lineChart = echarts.init(lineChartDom);
        var lineChartOption: EChartsOption;

        lineChartOption = {
          animation: false,
          title: {
            text: '连续样本指标变化曲线图'
          },
          tooltip: {
            trigger: 'axis'
          },
          legend: {
            // data: ['Email', 'Union Ads', 'Video Ads', 'Direct', 'Search Engine']
            left: 'center',
            top: '5%',
            bottom: '6%',
            data: indicatorKeys
          },
          grid: {
            left: '5%',
            right: '5%',
            bottom: '3%',
            containLabel: true
          },
          toolbox: {
            feature: {
              saveAsImage: {}
            }
          },
          xAxis: {
            type: 'category',
            boundaryGap: false,
            // data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            data: x_axis
          },
          yAxis: {
            type: 'value'
          },
          series: []
        };

        for (let key in indicator) {
          lineChartOption.series.push({
            name: key,
            type: 'line',
            stack: 'Total',
            data: indicator[key]
          })
        }
        lineChart.setOption(lineChartOption);

      }

    }
    
    // var lineChartDom = document.getElementById('indicatorVaryingFigure')!;
    

    // 绘制故障样本与非故障样本数量饼状图
    var pieChartDom = document.getElementById('faultExampleRatioFigure');
    if(!pieChartDom){
      console.log("faultDiagnosis pieChartDom is null")
      return 
    }
    let existingPieChart = echarts.getInstanceByDom(pieChartDom);

    if (!existingPieChart) {
      var pieChart = echarts.init(pieChartDom);
      var pieChartOption;

      pieChartOption = {
        title: {
          text: '预测结果中不同类型样本数量比例',
          // subtext: 'Fake Data',
          left: 'center'
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'vertical',
          left: 'left'
        },
        series: [
          {
            name: '样本数量',
            type: 'pie',
            radius: '50%',
            data: [
              {value: num_has_fault, name: '预测为故障类型的样本'},
              {value: num_has_no_fault, name: '预测为非故障类型的样本'},
              // { value: 580, name: 'Email' },
              // { value: 484, name: 'Union Ads' },
              // { value: 300, name: 'Video Ads' }
            ],
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            },
          }
        ],
        animation: false
      };
      pieChart.setOption(pieChartOption);
      var imgSrc = pieChart.getDataURL({
        type: 'png',  // 可选 'jpeg'
        backgroundColor: '#fff',
        excludeComponents: ['toolbox']
      })
      var img = imgSrc.split(',')[1]
      resultsToGenerateConclusion['faultDiagnosis']['imageBase64'] = img
    }
    
  })

  faultDiagnosisComplementaryFigure.value = 'data:image/png;base64,' + resultsObject.complementary_Base64
  faultDiagnosisComplementarySummary.value = resultsObject.complementary_summary


  faultDiagnosisResultsText.value = resultsObject.resultText
  // 向报告中添加故障诊断结果
  if (diagnosisResult == 0) {
    faultDiagnosis.value = '无故障'
    resultsToGenerateConclusion['faultDiagnosis']['text'] = '由输入的振动信号，共截取到'+(num_has_fault+num_has_no_fault)+
    '个样本，根据故障诊断模型预测，其中'+num_has_fault+'个样本存在故障，未达到样本总数的70%，由此判断该部件无故障'
  } else {
    faultDiagnosis.value = '存在故障'
    resultsToGenerateConclusion['faultDiagnosis']['text'] = '由输入的振动信号，共截取到'+(num_has_fault+num_has_no_fault)+
    '个样本，根据故障诊断模型预测，其中'+num_has_fault+'个样本存在故障，已达到样本总数的70%，由此判断该部件存在故障'
  }
  faultDiagnosisFigure.value = 'data:image/png;base64,' + figure1

}





// 故障预测结果展示
const displayFaultRegression = ref(false)
const generateFaultRegressionFigure = ref(false)
const haveFault = ref(0)
const faultRegression = ref('')
const timeToFault = ref('')
const faultRegressionFigure = ref('')

// const faultRegressionDisplay = (resultsObject) => {
//   displayFaultRegression.value = true

//   let figure1 = resultsObject.figure_Base64
//   faultRegressionFigure.value = 'data:image/png;base64,' + figure1
//   // let fault_time = results_object.time_to_fault

//   if (resultsObject.time_to_fault == 0) {
//     haveFault.value = 1
//     faultRegression.value = '已经出现故障'
//   } else {
//     haveFault.value = 0
//     faultRegression.value = '还未出现故障'
//     timeToFault.value = resultsObject.time_to_fault_str
//   }

// }

const faultRegressionDisplay = async(resultsObject: any) => {
  // displayFaultRegression.value = true

  let predictionConclusion: string
  let figure1 = resultsObject.figure_Base64
  faultRegressionFigure.value = 'data:image/png;base64,' + figure1
  // let fault_time = results_object.time_to_fault

  if (resultsObject.time_to_fault == 0) {
    haveFault.value = 1
    faultRegression.value = '已经出现故障'
    predictionConclusion = '预测结果：' + resultsObject.prediction_conclusion
  } else {
    haveFault.value = 0
    faultRegression.value = '还未出现故障'
    timeToFault.value = resultsObject.time_to_fault_str
    predictionConclusion = '预测结果：' + resultsObject.prediction_conclusion
    predictionConclusion += ', ' + '预计故障时间：' + resultsObject.time_to_fault_str
  }

  resultsToGenerateConclusion['faultPrediction']['text'] = predictionConclusion
}






// 插值处理可视化
const activeName3 = ref('1')
const displayInterpolation = ref(false)
const generateInterpolationFigure = ref(false)
const interpolationFigures = ref([]) // 插值处理结果图像
const interpolationResultsOfSensors = ref([])   // 插值处理结果中有几个传感器

// const interpolationDisplay = (resultsObject: any) => {
//   displayInterpolation.value = true

//   let sensorId = 0
//   interpolationFigures.value.length = 0
//   interpolationResultsOfSensors.value.length = 0
//   for (const [key, value] of Object.entries(resultsObject)) {
//     sensorId += 1
//     interpolationFigures.value.push('data:image/png;base64,' + value)
//     interpolationResultsOfSensors.value.push({label: key.split('_')[0], name: sensorId.toString()})
//   }
//   // console.log('interpolationResultsOfSensors: ', interpolationResultsOfSensors)
//   // console.log('interpolationFigures: ', interpolationFigures)
//   // displayDenoise.value = true
// }

const interpolationDisplay = async(resultsObject: any) => {
  // displayInterpolation.value = true

  let sensorId = 0
  interpolationFigures.value.length = 0
  interpolationResultsOfSensors.value.length = 0
  for (const [key, value] of Object.entries(resultsObject)) {
    sensorId += 1
    interpolationFigures.value.push('data:image/png;base64,' + value)
    if (!resultsToGenerateConclusion['interpolation']['imageBase64']){
      resultsToGenerateConclusion['interpolation']['imageBase64'] = value
      resultsToGenerateConclusion['interpolation']['text'] = '插值处理结果'
    }
    interpolationResultsOfSensors.value.push({label: key.split('_')[0], name: sensorId.toString()})
  }
  // console.log('interpolationResultsOfSensors: ', interpolationResultsOfSensors)
  // console.log('interpolationFigures: ', interpolationFigures)
  // displayDenoise.value = true
}




// 无量纲化可视化
const activeName4 = ref('1')
const displayNormalization = ref(false)
const generateNormalizationFigure = ref(false)
const normalizationFormdataRaw = ref([])
const normalizationFormdataScaled = ref([])  // 无量纲的结果表格
const normalizationColumns = ref([])
const normalizationResultFigures = ref([])   // 无量纲结果图像
const normalizationResultsSensors = ref([])
const transformDataToFormdata = (features_with_name: any, columns: any, formdata: any) => {
  // 从后端返回的结果中提取出特征名称和特征值，并转化为表格数据
  let featuresName = features_with_name.features_name.slice()
  let featuresGroupBySensor = Object.assign(features_with_name.features_extracted_group_by_sensor)
  let datas = []        // 表格中每一行的数据
  featuresName.unshift('传感器')  // 表格的列名
  for (const sensor in featuresGroupBySensor) {
    let features_of_sensor = featuresGroupBySensor[sensor].slice()
    features_of_sensor.unshift(sensor)
    datas.push(features_of_sensor)
  }

  columns.value.length = 0
  featuresName.forEach(element => {
    columns.value.push({prop: element, label: element, width: 180})
  });

  // 转换数据为对象数组  
  formdata.value = datas.map((row, index) => {
    const obj = {};
    columns.value.forEach((column, colIndex) => {
      obj[column.prop] = row[colIndex];
    });
    return obj;
  });
}

const normalizationResultType = ref('table')   // 无量纲化的结果类型，table表示表格，figure表示图像

const normalizationDisplay = async(resultsObject: any) => {
  // displayNormalization.value = true

  let rawData = Object.assign({}, resultsObject.raw_data)
  let scaledData = Object.assign({}, resultsObject.scaled_data)

  // 无量纲化结果为表格数据
  if (resultsObject.datatype == 'table') {
    normalizationResultType.value = 'table'
    transformDataToFormdata(rawData, normalizationColumns, normalizationFormdataRaw)
    transformDataToFormdata(scaledData, normalizationColumns, normalizationFormdataScaled)
  }
  // 无量纲化的对象为信号序列，结果为信号序列的波形图
  else {
    normalizationResultType.value = 'figure'
    let sensorId = 0
    normalizationResultFigures.value.length = 0
    normalizationResultsSensors.value.length = 0
    for (const [key, value] of Object.entries(resultsObject)) {
      if (key == 'datatype') {
        continue
      }
      sensorId += 1
      normalizationResultFigures.value.push('data:image/png;base64,' + value)
      if (resultsToGenerateConclusion['normalization']['imageBase64']){
        resultsToGenerateCxonclusion['normalization']['imageBase64'] = value
        resultsToGenerateConclusion['normalization']['text'] = '无量纲化结果'
      }
      normalizationResultsSensors.value.push({label: key.split('_')[0], name: sensorId.toString()})
    }
  }
}






// 小波降噪可视化
const activeName2 = ref('1')
const displayDenoise = ref(false)
const generateDenoiseFigure = ref(false)
const denoiseFigures = ref([])  // 存放小波降噪结果图片

interface waveletResults {
  label: string;
  name: string;
}
const waveletResultsOfSensors = ref<waveletResults[]>([])  // 存放不同传感器的小波降噪结果

// const denoiseDisplay = (resultsObject) => {
//   console.log('results_object: ', resultsObject)
//   let sensorId = 0
//   denoiseFigures.value.length = 0
//   waveletResultsOfSensors.value.length = 0
//   for (const [key, value] of Object.entries(resultsObject)) {
//     sensorId += 1
//     denoiseFigures.value.push('data:image/png;base64,' + value)
//     waveletResultsOfSensors.value.push({label: key.split('_')[0], name: sensorId.toString()})
//   }
//   console.log('results_of_sensors: ', waveletResultsOfSensors)
//   console.log('denoiseFigures: ', denoiseFigures)
//   displayDenoise.value = true
// }

const denoiseDisplay = async(resultsObject: any) => {
  // console.log('results_object: ', resultsObject)
  let sensorId = 0
  denoiseFigures.value.length = 0
  waveletResultsOfSensors.value.length = 0
  for (const [key, value] of Object.entries(resultsObject)) {
    sensorId += 1
    denoiseFigures.value.push('data:image/png;base64,' + value)
    if (!resultsToGenerateConclusion['wavelet']['imageBase64']){
      resultsToGenerateConclusion['wavelet']['imageBase64'] = value
      resultsToGenerateConclusion['wavelet']['text'] = '信号经小波变换后所得结果'
    }
    waveletResultsOfSensors.value.push({label: key.split('_')[0], name: sensorId.toString()})
  }
  // console.log('results_of_sensors: ', waveletResultsOfSensors)
  // console.log('denoiseFigures: ', denoiseFigures)
  // displayDenoise.value = true
}

const displayRawDataWaveform = ref(false)
const rawDataWaveform = ref('')
const currentDataBrowsing = ref('')

// 用于生成最终报告的模型中各个模块运行结果
let resultsToGenerateConclusion = {
  'includedModules': [] as string[],
  'outline': "",
  'healthEvaluation': {'imageBase64': "", 'text': ""},
  'featureExtraction': {'imageBase64': "", 'text': ""},
  'featureSelection': {'imageBase64': "", 'text': ""},
  'faultDiagnosis': {'imageBase64': "", 'text': ""},
  'faultPrediction': {'imageBase64': "", 'text': ""},
  'interpolation': {'imageBase64': "", 'text': ""},
  'normalization': {'imageBase64': "", 'text': ""},
  'wavelet': {'imageBase64': "", 'text': ""},
}

const selectAllModuleToGenerateResult = ref(false)

// 处理全选输出结果的逻辑
const toggleSelectAll = () => {
  if (selectAllModuleToGenerateResult.value) {
    moduleResultToGenerateList.value = [...contentJson.schedule];
  } else {
    moduleResultToGenerateList.value = [];
  }
  // 去除“数据源”这一项
  moduleResultToGenerateList.value = moduleResultToGenerateList.value.filter(item => item !== '数据源');
};

const moduleResultToGenerateList = ref<string[]>([])
const outputConfigVisible = ref(false)

// 打开结果输出配置面板
const outputConfig = () => {
  if(!missionComplete.value){
    ElMessage({
      message: "无运行结果",
      type: 'error'
    })
    return;
  }
  moduleResultToGenerateList.value = []
  outputConfigVisible.value = true
  selectAllModuleToGenerateResult.value = false
}


let mapping = {
  '层次分析模糊综合评估': 'healthEvaluation',
  '层次朴素贝叶斯评估': 'healthEvaluation',
  '层次逻辑回归评估': 'healthEvaluation',
  '健康评估': 'healthEvaluation',
  '特征提取': 'featureExtraction',
  '特征选择': 'featureSelection',
  '故障诊断': 'faultDiagnosis',
  '故障预测': 'faultPrediction',
  '插值处理': 'interpolation',
  '无量纲化': 'normalization',
  '小波变换': 'wavelet'
}


// 生成总结报告pdf
const generateConclusion = async() => {
  // 生成所选模块的报告
  if(moduleResultToGenerateList.value.length === 0){
    ElMessage({
      message: '请选择生成报告中所包含的结果',
      type: 'warning'
    })
    return
  }
  // 将中文的模块名转换为英文
  resultsToGenerateConclusion.includedModules = moduleResultToGenerateList.value.map(item => mapping[item])
  // console.log('resultsToGenerateOutput: ', resultsToGenerateConclusion)
  resultsViewClear()
  canShowResults.value = true
  console.log("canShowResults: ", canShowResults.value)
  moduleResultToGenerateList.value.forEach(moduleName => {
    if (missionComplete.value){
      // console.log("moduleName: ", moduleName)
      
     generateResultsToDisplay(moduleName, false);
       // 输出结果总体描述
    
      // console.log('moduleResultToGenerateList: ', moduleResultToGenerateList.value)
    }else{
      ElMessage({
        message: '无运行结果',
        type: 'warning'
      })
      return
    }
  })
  var outline = "时间："+ new Date().toLocaleString() + "<br/>" + "数据集："+ usingDatafile.value + "<br/>" + "模型名称："+ modelLoaded.value + "<br/>" + "包含模块："+ contentJson.schedule.join(', ')
  // console.log('resultsToGenerateOutput: ', resultsToGenerateConclusion)
  resultsToGenerateConclusion.outline = outline
  let formData = new FormData()
  formData.append('resultsToGenerateOutput', JSON.stringify(resultsToGenerateConclusion))

  api.post('user/generate_conclusion/', formData, { responseType: 'blob' }).then((response: any) => {
    if (response.status === 200) {
      ElMessage({
        message: '生成总结报告成功',
        type: 'success',
      });
      downloadFile(response.data, 'report.pdf');
      // let conclusion = response.data.data
    }else {
      ElMessage({
        message: '生成总结报告失败, '+response.data.message,
        type: 'error',
      });
    }
  })
  .catch((error: any) => {
    console.log('生成总结报告失败：', error)
  })
}

// const downloadFile = (data: BlobPart, filename: string) => {
//   const blob = new Blob([data], { type: 'application/pdf' });
//   const url = window.URL.createObjectURL(blob);
//   const link = document.createElement('a');
//   link.href = url;
//   link.download = filename;
//   link.click();
//   window.URL.revokeObjectURL(url);
// } 
// 生成报告后自动下载报告
const downloadFile = (blobData: Blob, fileName: string)=> {
  const url = window.URL.createObjectURL(new Blob([blobData]));
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', fileName); // 设置下载的文件名
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

const resultsViewClear = () => {
  showPlainIntroduction.value = false  // 清除算法介绍
  showStatusMessage.value = false      // 清除程序运行状态
  canShowResults.value = false         // 清除可视化区域元素
  contrastVisible.value = false    // 清除
  show1.value = true
  loading.value = true
  isShow.value = false
  // 清除所有结果可视化
  displayHealthEvaluation.value = false
  displayFeatureExtraction.value = false
  displayFeatureSelection.value = false
  displayFaultDiagnosis.value = false
  displayFaultRegression.value = false
  displayInterpolation.value = false
  displayNormalization.value = false
  displayDenoise.value = false
  displayRawDataWaveform.value = false

  // 重置报告生成配置
  generateFeatureExtractionFigure.value = false
  generateHealthEvaluationFigure.value = false
  generateFaultDiagnosisFigure.value = false
  generateFeatureSelectionFigure.value = false
  generateDenoiseFigure.value = false
  generateNormalizationFigure.value = false
  generateInterpolationFigure.value = false
  generateFaultRegressionFigure.value = false

  currentDisplayedItem = ''
  // if (!done.value) {
  // }
}

// 当前显示的算法模块结果
let currentDisplayedItem = ''

const generateResultsToDisplay = async(moduleName: string, display: boolean) => {
  if (moduleName == '层次分析模糊综合评估') {
      let results_to_show = responseResults.层次分析模糊综合评估
      if (currentDisplayedItem != '层次分析模糊综合评估' && display) {
        currentDisplayedItem = '层次分析模糊综合评估'
        displayHealthEvaluation.value = display  // 显示健康评估结果
        await healthEvaluationDisplay(results_to_show)
      } else {
        if (display && currentDisplayedItem == '层次分析模糊综合评估'){
          displayHealthEvaluation.value = display  // 显示健康评估结果
        }
        if (!display) {
          generateHealthEvaluationFigure.value = true
          await healthEvaluationDisplay(results_to_show)
        }
      }
    } else if (moduleName == '特征提取') {
      let results_to_show = responseResults.特征提取
      if (currentDisplayedItem != '特征提取' && display) {
        currentDisplayedItem = '特征提取'
        displayFeatureExtraction.value = display
        await featureExtractionDisplay(results_to_show)
      } else {
        if(display && currentDisplayedItem == '特征提取'){
          displayFeatureExtraction.value = display  // 显示特征提取结果
        }
        if(!display){
          generateFeatureExtractionFigure.value = true
          // displayFeatureExtraction.value = display
          featureExtractionDisplay(results_to_show)
        }
      }
    } else if (moduleName == '特征选择') {
      let results_to_show = responseResults.特征选择
      if (currentDisplayedItem != '特征选择' && display) {
        currentDisplayedItem = '特征选择'
        displayFeatureSelection.value = display
        await featuresSelectionDisplay(results_to_show)
      } else {
        if(display && currentDisplayedItem == '特征选择'){
          displayFeatureSelection.value = display  // 显示特征选择结果
        }
        if(!display){
          generateFeatureSelectionFigure.value = true
          featuresSelectionDisplay(results_to_show)
        }
      }
      
    } else if (moduleName == '故障诊断') {
      let results_to_show = responseResults.故障诊断
      if (currentDisplayedItem != '故障诊断' && display) {
        currentDisplayedItem = '故障诊断'
        displayFaultDiagnosis.value = display
        await faultDiagnosisDisplay(results_to_show)
      } else {
        if(display && currentDisplayedItem == '故障诊断'){
          displayFaultDiagnosis.value = display
        }
        if(!display){
          generateFaultDiagnosisFigure.value = true
          console.log("generateFaultDiagnosisFigure: ", generateFaultDiagnosisFigure.value)
          await faultDiagnosisDisplay(results_to_show)
        }
      }
    } else if (moduleName == '故障预测') {
      let results_to_show = responseResults.故障预测
      if (currentDisplayedItem != '故障预测' && display) {
        currentDisplayedItem = '故障预测'
        displayFaultRegression.value = display
        await faultRegressionDisplay(results_to_show)
      }else{
        if(display && currentDisplayedItem == '故障预测'){
          displayFaultRegression.value = display
        }
        if(!display){
          // 仅生成报告所需图片结果而不显示
          generateFaultRegressionFigure.value = true
          faultRegressionDisplay(results_to_show)
        }
      }
    } else if (moduleName == '插值处理') {
      let results_to_show = responseResults.插值处理
      if (currentDisplayedItem != '插值处理' && display) {
        currentDisplayedItem = '插值处理'
        displayInterpolation.value = display
        await interpolationDisplay(results_to_show)
      }else{
        if(display && currentDisplayedItem == '插值处理'){
          displayInterpolation.value = display
        }
        if(!display){
          // 仅生成报告所需图片结果而不显示
          generateInterpolationFigure.value = true
          interpolationDisplay(results_to_show)
        }
      }
    } else if (moduleName == '无量纲化') {
      let results_to_show = responseResults.无量纲化
      if (currentDisplayedItem != '无量纲化' && display) {
        currentDisplayedItem = '无量纲化'
        displayNormalization.value = display
        await normalizationDisplay(results_to_show)
      } else {
        if(display && currentDisplayedItem == '无量纲化'){
          displayNormalization.value = display
        }
        if(!display){
          // 仅生成报告所需图片结果而不显示
          generateNormalizationFigure.value = true
          normalizationDisplay(results_to_show)
        }
      }
    } else if (moduleName == '小波变换') {
      let results_to_show = responseResults.小波变换
      if (currentDisplayedItem != '小波变换' && display) {
        currentDisplayedItem = '小波变换'
        displayDenoise.value = display
        await denoiseDisplay(results_to_show)
      } else {
        if(display && currentDisplayedItem == '小波变换'){
          displayDenoise.value = display
        }
        if(!display){
          // 仅生成报告所需图片结果而不显示
          generateDenoiseFigure.value = true
          denoiseDisplay(results_to_show)
        }
      }
    } else if (moduleName == '层次朴素贝叶斯评估' ) {
      let results_to_show = responseResults.层次朴素贝叶斯评估
      if (currentDisplayedItem != '层次朴素贝叶斯评估' && display) {
        currentDisplayedItem = '层次朴素贝叶斯评估'
        displayHealthEvaluation.value = display
        await healthEvaluationDisplay(results_to_show)
      } else {
        if(display && currentDisplayedItem == '层次朴素贝叶斯评估'){
          displayHealthEvaluation.value = display
        }
        if(!display){
          // 仅生成报告所需图片结果而不显示
          generateHealthEvaluationFigure.value = true
          healthEvaluationDisplay(results_to_show)
        }
      }
      
      
    } else if (moduleName == '层次逻辑回归评估') {
      let results_to_show = responseResults.层次逻辑回归评估
      if (currentDisplayedItem != '层次逻辑回归评估' && display) {
        currentDisplayedItem = '层次逻辑回归评估'
        displayHealthEvaluation.value = display
        await healthEvaluationDisplay(results_to_show)
      } else {
        if(display && currentDisplayedItem == '层次逻辑回归评估'){
          displayHealthEvaluation.value = display
        }
        if(!display){
          // 仅生成报告所需图片结果而不显示
          generateHealthEvaluationFigure.value = true
          healthEvaluationDisplay(results_to_show)
        }
      }
    } else if (moduleName == '健康评估') {
      let results_to_show = responseResults.健康评估
      if (currentDisplayedItem != '健康评估' && display) {
        currentDisplayedItem = '健康评估'
        displayHealthEvaluation.value = display
        await healthEvaluationDisplay(results_to_show)
      } else {
        if(display && currentDisplayedItem == '健康评估'){
          displayHealthEvaluation.value = display
        }
        if(!display){
          // 仅生成报告所需图片结果而不显示
          generateHealthEvaluationFigure.value = true
          healthEvaluationDisplay(results_to_show)
        }
      }
      
    } else if (moduleName == '数据源'){
      ElMessage.warning("数据源无运行结果")
    } else {
      ElMessage({
        message: '无效的算法模块',
        type: 'error'
      })
    }
}

const showResult = (moduleName: string) => {

  if (missionComplete.value) {
    resultsViewClear()
    canShowResults.value = true
    generateResultsToDisplay(moduleName, true)
    setTimeout(function() {
      console.log('继续执行代码');
      generateResultsToDisplay(moduleName, false);
    }, 3000); // 暂停3秒
    console.log('moduleResultToGenerateList: ', moduleResultToGenerateList.value)
  }else{
    ElMessage.warning("无运行结果")
  }
  
}



// 从后端获取到的历史模型的信息
const fetchedModelsInfo = ref([])


const isFullScreen = ref(false);

//全屏
const toggleFullscreen = () => {
  if (document.fullscreenElement) {
    document.exitFullscreen();
    isFullScreen.value = false;
  } else {
    document.documentElement.requestFullscreen();
    isFullScreen.value = true;
  }
}


// 复用历史模型，不需要进行模型检查等操作
let modelHasBeenSaved = false
const modelLoaded = ref('无')  // 已加载的历史模型
let modelLoadedId = ''

//恢复画布
function restoreCanvas(objects) {

  if (objects.nodeList) {
    fromObject(objects.nodeList)
  }
  handleClear()
  updateStatus('当前模型已保存')
  modelHasBeenSaved = true
  canStartProcess.value = false

  console.log('使用的模型信息，并根据此再次构建contentjson',objects)

  console.log('边的信息:', modeling_nodeList.value)
  buildContentJson()
  // saveModelSetting(false, connection)
  console.log('objects.connection:', objects.connection)
  contentJson.schedule = objects.connection
  modelSetup.value = true
}

// // 点击历史模型表格中使用按钮复现用户历史模型
// const useModel = (row) => {
//   modelLoaded.value = row.model_name
//   //后端传来的数据恢复画布信息
//   // let objects = JSON.parse(row.model_info)
//   //要执行两遍才会渲染上
//   restoreCanvas(objects)
//   console.log('第一次渲染:', modeling_nodeList.value)
//   // 使用setTimeout等待0.5秒
//   setTimeout(() => {
//     // 0.5秒后执行的操作

//     restoreCanvas(objects)
//     console.log('第二次渲染:', modeling_nodeList.value)
//   }, 500);

// }


let index = 0
let row = 0
const deleteModelConfirmVisible = ref(false)
// 删除模型操作
const deleteModel = (indexIn, rowIn) => {
  index = indexIn
  row = rowIn
  deleteModelConfirmVisible.value = true
}
// 用户删除模型操作确认
const deleteModelConfirm = () => {

  // 发送删除请求到后端，row 是要删除的数据行
  api.get('/user/delete_model/?row_id=' + row.id).then((response) => {
    if (response.data.code == 401) {
      ElMessageBox.alert('登录状态失效，请重新登陆', '提示',
          {
            confirmButtonText: '确定',
            callback: (action: Action) => {
              router.push('/')
            }
          }
      )
    }
    if (response.data.code == 200) {
      // 如果被删除的模型已经被加载，则需要取消加载
      if (modelLoaded.value == row.model_name) {
        modelLoaded.value = '无'
        modelHasBeenSaved = false
        canStartProcess.value = true
        handleClear()
      }
      if (index !== -1) {
        // 删除前端表中数据
        fetchedModelsInfo.value.splice(index, 1)
        deleteModelConfirmVisible.value = false
        ElMessage({
          message: '删除模型成功',
          type: 'success'
        })
      }

    } else {
      if (response.data.code == 404) {
        ElMessage({
          message: '没有权限删除该模型',
          type: 'error'
        })
      } else {
        ElMessage({
          message: '删除模型失败，请稍后重试',
          type: 'error'
        })
      }
    }
  }).catch(error => {
    // 处理错误
    console.error(error);
    ElMessage({
      message: '删除模型失败,' + error,
      type: 'error'
    })
  });
}

// 查看模型的具体信息，按如下方式构造信息卡片
const modelName = ref('')
const modelAlgorithms = ref([])
const modelParams = ref([])  // {'模块名': xx, '算法': xx, '参数': xx}

const showModelInfo = (row) => {
  let objects = JSON.parse(row.model_info)
  let nodesList = objects.nodeList         // 模型节点信息
  let connection = objects.connection     // 模型连接顺序

  modelName.value = row.model_name
  modelAlgorithms.value = connection
  modelParams.value.length = 0
  nodesList.forEach(element => {
    let item = {'模块名': '', '算法': ''}
    item.模块名 = element.label
    item.算法 = labelsForAlgorithms[element.use_algorithm]
    modelParams.value.push(item)
  });
}

// 用于显示程序运行的状态信息
const showStatusMessage = ref(false)
const statusMessageToShow = ref('')

// 程序运行状态信息
const statusMessage = {
  'success': '## 程序已经运行完毕，请点击相应的算法模块查看对应结果！',
  'shutdown': '## 程序运行终止，点击清空模型重新建立模型',
  'error': '## 程序运行出错，请检查模型是否正确，或者检查加载的数据是否规范，点击清空模型重新建立模型',
}


// 控制是否可以修改模型，值为true时，可以修改模型，值为false时，不能修改模型
const toRectifyModel = ref(false)

// 完成建模
const finishModeling = () => {
  if (nodeList.value.length) {
    if (linkedList.length() == 0 && nodeList.value.length == 1) {
      ElMessage({
        message: '完成建模',
        type: 'success'
      })
      canCheckModel.value = false
      modelSetup.value = true     // 不能删除建模区的模块
      done.value = true           // 不能拖动模块
      toRectifyModel.value = true // 可以点击修改模型进行修改模型
      updateStatus('模型建立完成，请点击模型检查')
      return
    }
    if (linkedList.length() != nodeList.value.length) {
      ElMessage({
        message: '请确保图中所有模块均已建立连接，且没有多余的模块',
        type: 'warning'
      })
      return
    }
  }

  ElMessage({
    message: '完成建模',
    type: 'success'
  })
  modelSetup.value = true     // 不能删除建模区模块
  done.value = true     // 不能拖动模块
  toRectifyModel.value = true // 可以修改模型
  canCheckModel.value = false
  updateStatus('模型建立完成，请点击模型检查')
}

// 修改模型
const rectifyModel = () => {
  canCheckModel.value = true
  canSaveModel.value = true
  canStartProcess.value = true
  canShutdown.value = true
  modelSetup.value = false     // 可以删除建模区模块
  done.value = false     // 可以拖动模块
  toRectifyModel.value = false
  ElMessage({
    showClose: true,
    message: '进行模型修改, 完成修改后请再次点击完成建模',
    type: 'info'
  })
  updateStatus('正在修改模型')
}

//检查模型
const checkModeling = () => {
  if (nodeList.value.length == 0 && !modelHasBeenSaved) {
    canCheckModel.value = true
  }
}

//保存模型
const saveModeling = () => {
  if (nodeList.value.length == 0 || modelHasBeenSaved) {
    canSaveModel.value = true
  }
}

//开始建模
const startModeling = () => {
  if (nodeList.value.length == 0) {
    canStartProcess.value = true
  }
}


// 建模状态更新
function updateStatus(status) {
  var indicator = document.getElementById('statusIndicator');
  indicator.textContent = status; // 更新文本
  indicator.classList.remove('error', 'success', 'saved', 'rectify'); // 移除之前的状态类
  switch (status) {
    case '未建立模型':
      // 默认样式，或者设置为特定类
      break;
    case '请建立模型并点击检查模型':
      indicator.classList.add('error');
      break;
    case '模型建立并已通过模型检查':
      indicator.classList.add('success');
      break;
    case '当前模型已保存':
      indicator.classList.add('saved');
    case '正在修改模型':
      indicator.classList.add('rectify')
      break;
  }
}


const fetchedDataFiles = ref<Object[]>([])

// 用户目前选择的数据文件
const usingDatafile = ref('无')

const deleteDatasetConfirmVisible = ref(false)
let rowDataset: any = null
let indexDataset: any = null


// 用户删除历史数据
// const deleteDataset = (index_in: any, row_in: any) => {
//   indexDataset = index_in
//   rowDataset = row_in
//   deleteDatasetConfirmVisible.value = true
// }
// 确认删除历史数据文件
const deleteDatasetConfirm = (index: any, row: any) => {

  api.get('/user/delete_datafile/?filename=' + row.dataset_name)
      .then((response: any) => {
        if (response.data.code == 200) {
          // 删除前端表中数据
          fetchedDataFiles.value.splice(index, 1)
          deleteDatasetConfirmVisible.value = false
          ElMessage({
            message: '文件删除成功',
            type: 'success'
          })
          // 如果文件已经被加载，则需要取消加载行为
          if (rowDataset.dataset_name == usingDatafile.value) {
            usingDatafile.value = '无'
          }
        } else if (response.data.code == 400) {
          ElMessage({
            message: '删除失败: ' + response.data.message,
            type: 'error'
          })
        } else if (response.data.code == 401) {
          ElMessageBox.alert('登录状态已失效，请重新登陆', '提示', {
            confirmButtonText: '确定',
            callback: (action: Action) => {
              router.push('/')
            },
          })
        }
      })
      .catch((error: any) => {
        // console.log('delete_datafile_error: ', error)
        // ElMessage({
        //   message: '删除失败',
        //   type: 'error'
        // })
      })
}


// 用户选择历史数据进行加载
const useDataset = (row_in: any) => {
  loadingData.value = true
  setTimeout(() => {
    loadingData.value = false
    usingDatafile.value = row_in.dataset_name
    ElMessage({
      message: '数据加载成功',
      type: 'success'
    })
  }, 1000)

}


// 按关键字搜索用户数据文件
const searchDataset = () => {
  api
    .get("user/search_dataset/?keywords=" + searchDataKeyword.value)
    .then((response: any) => {
      if (response.data.code == 401) {
        ElMessageBox.alert("登录状态已失效，请重新登陆", "提示", {
          confirmButtonText: "确定",
          callback: () => {
            router.push("/");
          },
        });
      } else if (response.data.code == 200) {
        fetchedDataFiles.value.length = 0;
        for (let item of response.data.data) {
          fetchedDataFiles.value.push(item);
        }
      }
    })
    .catch(() => {
      // message.error("搜索失败，请重试");
      ElMessage({
        message: "搜索失败，请重试",
        type: "error",
      });
    });
};

// const handleSwitchDrawer = (fetchData: any[]) => {

//   modelsDrawer.value = false;

//   fetchedDataFiles.value = []
//   // fetchData.forEach(element => {
//   //   fetchedDataFiles.value.push(element)
//   // });
//   for (let item of fetchData){
//     fetchedDataFiles.value.push(item)
//   }

//   dataDrawer.value = true

//   // Object.assign(fetchedDataFiles, fetchData)
// };


// 已加载模型和已加载数据字体颜色更改
const getColor = (value: string) => {
  if (value == '无') {
    return 'red'
  } else {
    return 'green'
  }
}
</script>

<style>
body {
  margin: 0;
}


.item {
  width: 150px;
  height: 50px;
  position: relative;
}

.deleteButton {
  position: absolute;
  top: 2px;
  right: 2px;
}

#source {
  border: 2px solid red;
}

#target {
  border: 2px solid blue;
}

.main {
  display: flex;
}

ul {
  list-style: none;
  padding-left: 0;
  width: 120px;
  background: #eee;
  text-align: center;
}

ul > li {
  height: 40px;
  line-height: 40px;
}

.main-right {
  border: 1px solid #ccc;
  flex: 1;
  margin-left: 15px;
  position: relative;
  background: #f4f4f4;
}

.node-info {
  position: relative;
  top: 5px
}

.node-info-label {
  /* font-style: italic; */
  /* 垂直和水平居中的样式 */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  white-space: normal;
  overflow: visible;
  /* font-style: italic; */
  padding: 4px;
  position: relative;
  width: 180px;
  height: 70px;
  /* line-height: 36px; */
  font-size: 12px;
  text-align: center;
  border: 1px solid #e5e7eb;
  background: #fff;

}

.node-info-label:hover {

  cursor: pointer;
  background: #f4eded;
}

.node-info-label:hover + .node-drag {
  /* background: red; */
  display: inline-block;
}

.node-drag {
  width: 10px;
  height: 10px;
  border-radius: 10px;
  background-color: gray;
  border: 1px solid #ccc;
  position: absolute;
  right: -7px;
  top: 50%;
  transform: translateY(-50%);
}

.node-drag:hover {
  display: inline-block;

}

.fullscreen_container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.result_visualization_view {
  width: 1200px;
  height: 600px;
  position: absolute;
}

.demo-tabs .custom-tabs-label span {
  vertical-align: middle;
  font-size: 16px;
  margin-left: 9px;
}

.status-indicator {
  position: absolute;
  top: 8%;
  left: 2%;
  padding: 5px 10px;
  border-radius: 5px;
  border: solid 1px rgba(0, 0, 0, 0.2);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  background-color: #cbd1ceea;
  font-size: 20px;
  font-weight: 700;
  font-family: 'Microsoft YaHei';
  /* 初始颜色，如黄色 */
  color: rgb(26, 48, 27);
  z-index: 1000;
  /* 确保它显示在其他元素之上 */
}

/* 可以为不同的状态添加额外的类 */
.status-indicator.error {
  background-color: #e0b75f;
  /* 红色表示错误或未通过检查 */
}

.status-indicator.success {
  background-color: #5cb85c;
  /* 绿色表示成功 */
}

.status-indicator.saved {
  background-color: #337ab7;
  /* 蓝色表示已保存 */
}

.status-indicator.rectify {
  background-color: #48a4a3;
  /* 表示正在修改模型 */
}

html,
body {
  height: 100vh;
  margin: 0;
  /* 移除默认的边距 */
  padding: 0;
  /* 移除默认的内边距 */
}

.el-main {
  background-color: #CCD0D6;
  /*color: #333;*/
  text-align: center;
  position: relative;
  background-position: center;
  background-size: contain;
  /* height: 50vh; */
  background-repeat: no-repeat;
}

.has-background {
  background-color: #CCD0D6;
  /*color: #333;*/
  text-align: center;
  position: relative;
  background-image: url('../assets/modeling.png');
  background-position: center;
  background-size: contain;
  /* height: 50vh; */
  background-repeat: no-repeat;
}

.clickable:hover {
  cursor: pointer;
  color: #007BFF;
}

.aside-title {
  font-size: 20px;
  font-weight: 700;
  background-color: #ebeef4;
  justify-content: center;
  display: flex;
  align-items: center;
  gap: 5px;
  border-top: solid 3px #7D8081;

  text-align: center;
  width: 100%;
  height: 50px;
  color: #093256;
}

.first-menu-item {
  width: 150px;
  margin-top: 10px;
  background-color: #4C74DA;
  color: white;
}

.second-menu-item {
  width: 150px;
  margin-top: 7px;
  background-color: #7E9CE6;
}

.third-menu-item {
  background-color: #B9BFCE;
  margin-top: 7px;
  width: 145px;
  height: 30px;
  margin-bottom: 10px;
  padding: 0px;
  border-radius: 5px;
  align-content: center;
  margin-left: 40px;
}

.el-icon-devops {
  background: url('../assets/userModels.svg') center no-repeat;
  font-size: 12px;
  background-size: cover;
}

/* .el-space {
  display: flex;
  justify-content: center;
  align-items: center;
} */

.operation-button {
  /* margin: 0 5px; */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.operation-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}


.menuList-First {
  width: 150px;
  margin-top: 10px;
  background-color: #063e66;
  color: white;
}

.menuList-Second {
  width: 150px;
  margin-top: 10px;
  background-color: #2869C7;
  color: white;
}

/* 修改单选按钮选中状态的颜色 */
.ant-radio-button-wrapper-checked {
  color: #fff;
  background-color: #da222a;
  border-color: #da222a;
}

/* 修改单选按钮未选中状态的颜色 */
.ant-radio-button-wrapper {
  border-color: #da222a; /* 可以改变未选中时的边框颜色 */
}

/* 修改单选按钮组内的按钮之间的分隔线颜色 */
.ant-radio-button-wrapper:not(:last-child)::after {
  background-color: #da222a;
}

/* 修改单选按钮悬停时的颜色 */
.ant-radio-button-wrapper:hover {
  color: #fff;
  background-color: #c71e26;
  border-color: #c71e26;
}

.text-button {
  background: none;
  border: none;
  color: #333;
  font-family: 'Arial', sans-serif;
  font-size: 18px;
  padding: 10px 20px;
  cursor: pointer;
  transition: color 0.3s, border-bottom 0.3s;
}

.text-button.active {
  color: #007bff;
  border-bottom: 2px solid #007bff;
}

.module-name {
  width: 100%; /* 设置固定的宽度 */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.custom-radio-button:hover {
  background-color: #c4e8ba;

}
</style>

<style scoped lang="scss">
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #c1ced9;
  padding: 0 20px;
  height: 60px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1),
  0 1px 3px rgba(0, 0, 0, 0.08);
  text-align: center;
  line-height: 60px;
  position: relative;
  margin-top: 1px;
  width: 100%;
}

.logo {
  display: flex;
  flex: 4;
  align-items: center;
  justify-content: flex-start;
  font-size: 22px;
}

.logo img {
  height: 36px;
  margin-right: 12px;
}

.logo-text {
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
}

.title {
  flex-grow: 1;
  display: flex;
  flex: 4;
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  height: 60px;
}

.title h1 {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: #333;
  font-family: 'JetBrains Mono', monospace;
  height: 60px;
  white-space: nowrap; /* 不换行 */
  overflow: hidden; /* 隐藏溢出部分 */
}

.user-actions {
  display: flex;
  flex: 4;
  align-items: center;
  justify-content: flex-end;
  margin-right: 0;
}

.welcome-message {
  font-size: 16px;
  font-family: 'Microsoft YaHei';
  //color: #409EFF;
  color: black;
  margin-right: 18px;
  white-space: nowrap; /* 不换行 */
  overflow: hidden; /* 隐藏溢出部分 */
}

.action-item {
  display: flex;
  font-family: 'Microsoft YaHei';
  align-items: center;
  margin-right: 18px;
  cursor: pointer;
}

.action-item .action-icon {
  font-size: 16px;
  margin-right: 5px;
  //color: #409EFF;
  color: black;
}

.action-item .action-text {
  font-size: 16px;
  //color: #409EFF;
  color: black;
}

.action-item:hover .action-icon,
.action-item:hover .action-text {
  color: #66b1ff;
}

.action-item:hover .action-icon {
  transform: scale(1.2);
  transition: transform 0.3s;
}

/*
使用 Font Awesome 图标:
1、安装：
npm install @fortawesome/fontawesome-free
2、配置：
// 在要使用的地方 导入 Font Awesome CSS
// 网站：https://fontawesome.com/icons
import '@fortawesome/fontawesome-free/css/all.css';
*/
//@import 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css';

//tree css start
.custom-tree-node {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
  //padding-right: 8px;
  //background-color: #5cb85c;
}

.node-label {
  //background-color: red;
}

.node-actions {
  display: flex;
  align-items: center;
  justify-content: center;
  //background-color: #3c93f8;
  gap: 8px;
  margin-left: 8px;
}

.el-button {
  font-size: 12px;
  padding: 0 5px;
}

.el-tree .el-tree-node__content {
  padding: 5px 10px;
  border-radius: 4px;
}

.el-tree .el-tree-node__content:hover {
  background-color: #f0f0f0;
}

//tree css end
//el-main分割 css start
.parent-containerOfElMain {
  position: relative;
  width: 100%;
  //height: 100vh;
  height: 100%;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  padding: 0;
}

/* 建模部分 */
.modeling-areaOfElMain {
  flex: 1;
  background-color: #ffffff;
  padding: 0;
  overflow: auto;
  width: 100%;
  height: 100%;
  z-index: 1;
}

/* 运行结果部分 */
.result-areaOfElMain {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  background-color: #ffffff;
  //border-top: 2px solid #409EFF;
  z-index: 1;
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden; /* 确保内容在高度变化时不溢出 */
}

/* 运行结果头部，可拖动 */
.result-headerOfElMain {
  cursor: ns-resize;
  padding: 0;
  width: 100%;
  height: 40px;
  background-color: #ebeef4;
  color: #409EFF;
  display: flex;
  justify-content: space-between;
  align-items: center;
  user-select: none;
  position: relative;
}

/* 运行结果内容 */
.result-contentOfElMain {
  padding: 0;
  //overflow: auto;
  overflow-y: hidden;
  flex-grow: 1;
  height: 100%
}

.buttonsOfElMain {
  width: 100%;
  display: flex;
  justify-content: end;
}

/* 控制按钮 */
.control-buttonsOfElMain {
  position: absolute;
  bottom: 0;
  //background-color: #66e748;
  left: 0;
  z-index: 3;
  display: flex;
  gap: 10px;
}

/* 图标按钮样式 */
.icon-buttonOfElMain {
  background: none;
  border: none;
  margin-right: 10px;
  //color: #000000;
  cursor: pointer;
  font-size: 18px; /* 调整图标大小 */
  padding: 5px;
  transition: color 0.3s ease, background-color 0.3s ease;
  //border-radius: 50%; /* 添加圆角 */
}

.icon-buttonOfElMain:hover {
  color: #000000;
  background-color: rgba(235, 238, 244, 0.1); /* 添加悬停背景 */
}

.icon-buttonOfElMain.primary {
  color: #409EFF;
}

.icon-buttonOfElMain.success {
  color: #67c23a;
}

/* 过渡动画 */
.slide-enter-active,
.slide-leave-active {
  transition: opacity 0.5s ease, transform 0.5s ease;
}

.slide-enter-from {
  opacity: 0;
  transform: translateY(100%); /* 从下往上 */
}

.slide-enter-to {
  opacity: 1;
  transform: translateY(0);
}

.slide-leave-from {
  opacity: 1;
  transform: translateY(0);
}

.slide-leave-to {
  opacity: 0;
  transform: translateY(100%); /* 从上往下 */
}

//el-main分割 css end

//自定义侧边栏样式start
.el-aside-demo {
  background: white;
  overflow-y: auto;
  overflow-x: hidden;
  margin-right: 1px;
  box-shadow: 3px 0 3px rgba(0, 0, 0, 0.2);
  z-index: 2;
  width: 250px;
  align-items: center;
  font-family: 'Microsoft YaHei', sans-serif; // 添加字体属性
}

.aside-title {
  font-size: 25px;
  color: #34374f;
  border: rgb(204, 208, 214) 1px solid;
  width: 100%;
  font-family: 'Microsoft YaHei', sans-serif; // 添加字体属性
}

/* 滚动条轨道样式 */
.el-aside-demo::-webkit-scrollbar-track {
  -webkit-box-shadow: inset 0 0 6px rgba(255, 255, 255, 0);
  background-color: #ebeef4; /* 更深的颜色，让轨道看起来更清晰 */
  border-radius: 10px; /* 圆角轨道 */
}

/* 整体滚动条样式 */
.el-aside-demo::-webkit-scrollbar {
  width: 0; /* 设置滚动条的宽度 */
  background-color: #ffffff; /* 与轨道背景色一致 */
  border-radius: 10px; /* 圆角滚动条 */
}

/* 滚动条滑块样式 */
.el-aside-demo::-webkit-scrollbar-thumb {
  //background: linear-gradient(to top, rgba(125, 126, 128, 0.6), rgba(97, 98, 99, 0.6)); /* 渐变色效果 */
  border-radius: 10px; /* 圆角滑块 */
  border: 2px solid rgba(255, 255, 255, 0.2); /* 添加边框，以提高可视性 */
}

/* 滚动条滑块悬浮时的样式 */
.el-aside-demo::-webkit-scrollbar-thumb:hover {
  //background: linear-gradient(to top, rgba(125, 126, 128, 0.8), rgba(97, 98, 99, 0.8)); /* 鼠标悬浮时加深颜色 */
}

//自定义侧边栏样式end

//建模区域的配置菜单start
/* 配置区域 */
.configPanelOfModelNode {
  width: 300px;
  height: 100%;
  position: absolute;
  top: 0;
  right: 0;
  z-index: 1;
  background-color: white;
  transition: transform 0.3s ease-in-out;
  box-shadow: -3px 0 3px rgba(0, 0, 0, 0.2);
  overflow-x: hidden;
  overflow-y: hidden;
}

/* 隐藏配置区域时的transform */
.configPanelOfModelNode.hidden {
  transform: translateX(100%);
}

.closeConfigPanelBtnOfModelNode {
  width: 100%;
  display: flex;
  //margin-left: 10px;
  height: 35px;
  padding-left: 10px;
  justify-content: start;
  background-color: #ebeef4;
  border-bottom: #ccd0d6 solid 1px;
}

/* 配置区域初始状态 */
.configAreaPanelOfModelNode {
  height: 95%;
  display: flex;
  flex-direction: column;
  width: 100%;
  //background-color: #66e748;
  overflow-x: hidden;
  overflow-y: auto;
}

/* 滚动条轨道样式 */
.configAreaPanelOfModelNode::-webkit-scrollbar-track {
  -webkit-box-shadow: inset 0 0 6px rgba(255, 255, 255, 0);
  background-color: #ffffff;
  border-radius: 10px;
}

/* 整体滚动条样式 */
.configAreaPanelOfModelNode::-webkit-scrollbar {
  width: 8px;
  background-color: #ccd0d6;
  border-radius: 10px;
}

/* 滚动条滑块样式 */
.configAreaPanelOfModelNode::-webkit-scrollbar-thumb {
  //background: linear-gradient(to top, rgba(125, 126, 128, 0.6), rgba(97, 98, 99, 0.6)); /* 渐变色效果 */
  border-radius: 10px;
  border: 2px solid rgba(32, 130, 249, 0.2);
}

/* 滚动条滑块悬浮时的样式 */
.configAreaPanelOfModelNode::-webkit-scrollbar-thumb:hover {
  //background: linear-gradient(to top, rgba(125, 126, 128, 0.8), rgba(97, 98, 99, 0.8)); /* 鼠标悬浮时加深颜色 */
}

//建模区域的配置菜单end
.control-operator-btn-default-css {
  width: 61px;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}

.menu-item-first {
  font-family: 'Microsoft YaHei';
  font-size: 20px
}


.menu-item-second {
  font-family: 'Microsoft YaHei';
  font-size: 17px
}

</style>
