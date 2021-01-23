<template>
  <el-row>
    <el-col :span="6">
      <div style="margin-left: 20px;margin-top: 20px">
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span>权限分类</span>
            <el-button style="float: right; padding: 3px 0" type="text" @click="handleTopCreate">新建</el-button>
          </div>
          <div class="text item">
            <el-tree
              ref="tree"
              :data="queryDatalist"
              :props="defaultProps"
              node-key="id"
              @node-click="handleCheckChange"
            >
      <span class="custom-tree-node" slot-scope="{ node, data }">
        <span>{{ node.label }}</span>
        <span>
          <el-button
            type="text"
            size="mini"
            @click="() => edit(node,data)">
            编辑
          </el-button>
          <el-button
            type="text"
            size="mini"
            @click="() => remove(node, data)">
            删除
          </el-button>
        </span>
      </span>
            </el-tree>
          </div>
        </el-card>
      </div>
    </el-col>

    <el-col :span="18">
      <div>
        <el-card class="box-card" shadow="hover" style="margin: 20px">
          <div class="clearfix" slot="header">
            <span>权限明细</span>
          </div>
          <div v-if="flag === false">请选择左侧节点</div>
          <div v-else-if="nodeData.length === 0 || nodeData.length === undefined">节点暂无数据</div>
          <div v-else>
            <div class="filter-container">
              <el-button
                @click="handleCreate"
                class="el-button filter-item el-button--primary"
                icon="el-icon-edit"
                style="margin-left: 10px;height: 35px"
                type="primary"
              >
                新建
              </el-button>
            </div>
            <div class="text item">
              <el-table
                :data="nodeData"
                row-key="id"
                lazy
                border
                style="width: 100%"
                :tree-props="{children: 'children', hasChildren: 'hasChildren'}"
              >
                <el-table-column
                  label="序号"
                  type="index"
                  width="80">
                </el-table-column>
                <el-table-column align="left" label="权限名称">
                  <template slot-scope="scope">
                    {{ scope.row.title }}
                  </template>
                </el-table-column>

                <el-table-column align="left" label="权限标识">
                  <template slot-scope="scope">
                    {{ scope.row.slug }}
                  </template>
                </el-table-column>

                <el-table-column align="left" label="备注" style="height: 50px">
                  <template slot-scope="scope">
                    <el-popover
                      placement="bottom"
                      title="备注"
                      width="300"
                      trigger="click"
                      :content=scope.row.remarks>
                      <el-button slot="reference">点击查看</el-button>
                    </el-popover>
                  </template>
                </el-table-column>

                <el-table-column
                  label="操作"
                  align="center"
                  width="220">
                  <template slot-scope="scope">
                    <el-button type="primary" size="small" @click="handleEdit(scope)">编辑</el-button>
                    <el-button type="danger" size="small" @click="handleDelete(scope)">删除</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </div>
        </el-card>

        <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
          <el-form class="el-form" :model="tempData" :rules="rules">
            <el-form-item label="权限名称" label-width="80px" prop="title">
              <el-input v-model="tempData.title"></el-input>
            </el-form-item>
            <el-form-item label="权限标识" label-width="80px" prop="slug">
              <el-input v-model="tempData.slug"></el-input>
            </el-form-item>

            <el-form-item label="备注" label-width="80px">
              <el-input v-model="tempData.remarks"></el-input>
            </el-form-item>
            <el-form-item label="主菜单" label-width="80px">
              <el-switch v-model="switchStatus" @change="switchChange($event)"></el-switch>
            </el-form-item>
            <el-form-item
              v-if="dialogStatus==='update' &&  switchStatus === false && nodeStatus === true && nodeData.length === 0 "
              label="指定父级" label-width="80px">
              <el-select v-model="tempData.pid" placeholder="请选择">
                <el-option
                  v-for="item in queryDatalist"
                  :key="item.id"
                  :label="item.title"
                  :value="item.id">
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item
              v-else-if="dialogStatus==='update' && switchStatus === false && nodeStatus === true && nodeData.length > 0"
              label="指定父级" label-width="80px">
              <el-input
                placeholder="此节点下有数据不可作为子节点使用"
                :disabled="true">
              </el-input>
            </el-form-item>
            <el-form-item v-else-if="dialogStatus==='update' &&  switchStatus === false  " label="指定父级"
                          label-width="80px">
              <el-select v-model="tempData.pid" placeholder="请选择">
                <el-option
                  v-for="item in queryDatalist"
                  :key="item.id"
                  :label="item.title"
                  :value="item.id">
                </el-option>
              </el-select>
            </el-form-item>

            <el-form-item v-else-if="dialogStatus==='create' && switchStatus === false " label="指定父级"
                          label-width="80px">
              <el-select v-model="tempData.pid" placeholder="请选择">
                <el-option
                  v-for="item in queryDatalist"
                  :key="item.id"
                  :label="item.title"
                  :value="item.id">
                </el-option>
              </el-select>
            </el-form-item>
          </el-form>
          <div class="dialog-footer" slot="footer">
            <el-button @click="handleDownFormVisible()">取 消</el-button>
            <el-button @click="dialogStatus==='create'?createData():updateData()" type="primary">确 定</el-button>
          </div>
        </el-dialog>
      </div>
    </el-col>
  </el-row>
</template>

<script>
import {Message} from 'element-ui'
import {
  getPermissions,
  postPermissions,
  putPermissions,
  deletePermissions,
  detailsPermissions
} from "@/api/roles";


export default {
  name: 'permission-roles',

  data() {
    return {
      defaultProps: {
        children: 'children',
        label: 'title'
      },
      rules: {
        title: [{required: true, message: '名称必填', trigger: 'blur'}],
        slug: [{required: true, message: '标识必填', trigger: 'blur'}],
      },
      queryDatalist: [],
      dialogFormVisible: false,
      dialogStatus: 'update',
      textMap: {
        update: '更新信息',
        create: '创建部门'
      },
      tempData: [],
      switchStatus: false,
      nodeData: [],
      flag: false,  // 如果为 false 则没有点击左侧 tree 节点
      nodeStatus: false,
      nodeId: 0
    }
  },
  created() {
    this.GetList()
  },
  methods: {
    remove(node, data) {
      this.defeteFunc(data.id, data.pid)
    },
    edit(node, data) {
      this.tempData = {}
      this.nodeStatus = true
      this.dialogStatus = 'update'
      this.tempData = JSON.parse(JSON.stringify(data))
      this.switchStatus = true
      this.dialogFormVisible = true
    },
    handleCheckChange(data, checked, indeterminate) {
      this.flag = true
      this.getPerNodes(data.id)
      this.nodeId = data.id
    },
    GetList() {
      getPermissions({
        pid: 0
      }).then(response => {
        this.queryDatalist = response.data
      })
    },
    getPerNodes(pid) {
      getPermissions({
        pid: pid
      }).then(response => {
        this.nodeData = response.data
      })
    },
    handleEdit(scope) {
      this.nodeStatus = false
      this.dialogStatus = 'update'
      this.tempData = JSON.parse(JSON.stringify(scope.row))
      this.switchStatus = false
      this.dialogFormVisible = true
    },
    createData() {
      postPermissions(this.tempData).then((request) => {
        this.dialogFormVisible = false
        this.GetList()
        this.getPerNodes(this.nodeId)
        this.$notify({
          title: '成功',
          message: '创建数据成功!',
          type: 'success',
          duration: 2000
        })
      })
    },
    updateData() {
      if (this.tempData.id === this.tempData.pid) {
        Message.error('暂不支持节点绑定自己')
        this.dialogFormVisible = false
        this.GetList()
      } else {
        putPermissions(this.tempData, this.tempData.id).then(() => {
          this.dialogFormVisible = false
          this.GetList()
          this.getPerNodes(this.nodeId)
          this.$notify({
            title: '成功',
            message: '更新数据成功!',
            type: 'success',
            duration: 2000
          })
        })
      }

    },
    handleTopCreate() {
      this.switchStatus = true
      this.tempData = {
        'pid': 0
      }

      this.dialogStatus = 'create'
      this.dialogFormVisible = true
    },
    handleCreate() {
      this.tempData = {}
      this.switchStatus = false
      this.tempData.pid = this.nodeId
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
    },
    handleDownFormVisible() {
      this.tempData = Object.assign({}, deletePermissions)
      this.dialogFormVisible = false
    },
    // 删除
    handleDelete(scope) {
      this.defeteFunc(scope.row.id, scope.row.pid)
    },
    defeteFunc(id, pid) {
      this.$confirm('此操作将永久删除该数据, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        getPermissions({pid: id}).then((request) => {
          if (request.data.length === 0) {
            deletePermissions(id).then(() => {
              if (pid === 0) {
                this.GetList()
              } else {
                this.getPerNodes(pid)
              }
              this.$message({
                type: 'success',
                message: '删除成功!'
              })
            })
          } else {
            Message.error('节点有数据请清空数据后重试!')
            this.GetList()
            this.getPerNodes(id)
          }
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    },
    // 关闭抽屉
    cancelForm() {
      this.dialog = false
    },
    switchChange($event) {
      if ($event === true) {
        this.tempData.pid = 0
      } else {
        this.tempData.pid = ''
      }
    }
  },
}
</script>

<style>
.custom-tree-node {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
  padding-right: 8px;
}
</style>
