<template>


  <div>
  <el-card class="box-card" shadow="hover" style="margin: 20px">
    <div class="clearfix" slot="header">
      <span>菜单管理</span>
    </div>
    <div class="filter-container">
<!--      <el-input-->
<!--        @keyup.enter.native="searchFilter"-->
<!--        class="input-with-select"-->
<!--        clearable-->
<!--        placeholder="请输入搜索内容"-->
<!--        style="width: 500px">-->
<!--&lt;!&ndash;        v-model="pageQuerylist.search_content"&ndash;&gt;-->
<!--&lt;!&ndash;      >&ndash;&gt;-->
<!--        <el-button @click="searchFilter" icon="el-icon-search" slot="append"/>-->
<!--      </el-input>-->
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
      :data="queryDatalist"
      row-key="id"
      lazy
      :load="load"
      :tree-props="{children: 'childrens', hasChildren: 'hasChildren'}"
    >
      style="width: 100%;margin-top:30px;">
      <el-table-column align="center" label="菜单名称" width="220">
        <template slot-scope="scope">
          {{ scope.row.title }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="菜单路径" width="220">
        <template slot-scope="scope">
          {{ scope.row.url }}
        </template>
      </el-table-column>

      <el-table-column align="center" label="操作">
        <template slot-scope="scope">
          <el-button type="primary" size="small" @click="handleEdit(scope)">编辑</el-button>
          <el-button type="danger" size="small" @click="handleDelete(scope)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    </div>
  </el-card>
    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
    <el-form class="el-form" :model="tempData" :rules="rules">
      <el-form-item label="名称" label-width="80px" prop="name">
        <el-input v-model="tempData.title"  ></el-input>
      </el-form-item>
      <el-form-item label="标识" label-width="80px" prop="email">
        <el-input v-model="tempData.url" ></el-input>
      </el-form-item>

      <el-form-item label="菜单路径" label-width="80px">
        <el-input v-model="tempData.url" ></el-input>
      </el-form-item>
      <el-form-item label="父级菜单" label-width="80px">
        <el-switch v-model="switchStatus" @change="switchChange($event)"></el-switch>
      </el-form-item>
      <el-form-item v-if="switchStatus === false && nodeData.length !== 0" label="指定父级" label-width="80px">
        <el-input
        placeholder="此节点下有数据不可作为子节点使用"
        :disabled="true">
      </el-input>
      </el-form-item>
      <el-form-item  v-else-if="switchStatus === false && nodeData.length === 0" label="指定父级"   label-width="80px">
          <el-select  v-model="tempData.pid" placeholder="请选择">
              <el-option
                v-for="item in queryDatalist"
                :key="item.id"
                :label="item.title"
                :value="item.id">
              </el-option>
            </el-select>
      </el-form-item>

      <el-form-item label="绑定角色" label-width="80px">
          <el-select v-model="tempData.roles_list" class="selector" multiple placeholder="请选择">
            <el-option
              v-for="item in rolseList"
              :key="item.id"
              :label="item.title"
              :value="item.id"/>
          </el-select>

      </el-form-item>

    </el-form>
    <div class="dialog-footer" slot="footer">
      <el-button @click="handleDownFormVisible()">取 消</el-button>
      <el-button @click="dialogStatus==='create'?createData():updateData()" type="primary">确 定</el-button>

    </div>
  </el-dialog>
</div>
</template>

<script>
import { Message } from 'element-ui'
import { deepClone } from "@/utils";
import {
  getRoles
} from "@/api/roles";

import {
  getMenus,
  postMenus,
  putMenus,
  deleteMenus,
} from "@/api/roles";
const defaultMenu = {
  title: '',
  url: '',
  pid: 0,
  is_active: ''
}

export default {
  name: 'permission-roles',

  data() {
    return {

      rules: {
        title: [{ required: true, message: '名称必填', trigger: 'blur' }],
        slug: [{ required: true, message: '标识必填', trigger: 'blur' }],
        permissions: [{ required: true, message: '权限必选', trigger: 'blur' }],
      },
      queryDatalist: [],
      dialogFormVisible: false,
      dialogStatus: 'update',
      textMap: {
        update: '更新信息',
        create: '创建菜单'
      },
      dialog: false,
      tempData: [],
      rolseList: [],
      switchStatus: false,
      nodeData: [],
    }
  },
  created() {
    this.GetList()
    this.getRolesList()
  },
  methods: {
    handleGet() {

    },
    GetList() {
      getMenus({
        pid: 0
      }).then(response => {
        this.queryDatalist = response.data
      })
    },
    load(row, treeNode, resolve) {
      getMenus({ pid: row.id }).then((request) => {
        resolve(request.data)
      })
    },
    getMenuNodes(pid) {
      getMenus({
        pid: pid
      }).then(response => {
        this.nodeData = response.data
      })
    },
    getRolesList() {
      getRoles().then((request) => {
        this.rolseList = request.data
      })
    },
    handleEdit(scope) {
      this.tempData = JSON.parse(JSON.stringify(scope.row))
      this.getMenuNodes(this.tempData.id)
      if (scope.row.pid === 0) {
        this.switchStatus = true
      } else {
        this.switchStatus = false
      }
      // this.tempData = deepClone(scope.row)
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
    },
    createData() {
      console.log(this.tempData)
      postMenus({
        title: this.tempData.title,
        slug: this.tempData.slug,
        url: this.tempData.url,
        roles: this.tempData.roles_list,
        pid: this.tempData.pid
      }).then((request) => {
        this.dialogFormVisible = false
        this.queryDatalist = []
        this.GetList()
        this.$notify({
          title: '成功',
          message: '创建数据成功!',
          type: 'success',
          duration: 2000
        })
      })
    },
    updateData() {
      var jsonParams = {
        title: this.tempData.title,
        slug: this.tempData.slug,
        url: this.tempData.url,
        roles: this.tempData.roles_list,
        pid: this.tempData.pid
      }
      if (this.tempData.id === this.tempData.pid) {
        Message.error('暂不支持节点绑定自己')
        this.dialogFormVisible = false
        this.queryDatalist = []
        this.GetList()
      } else {
        putMenus(jsonParams, this.tempData.id).then(() => {
          this.dialogFormVisible = false
          this.queryDatalist = []
          this.GetList()
          // this.getMenuNodes(this.tempData.id)
          this.$notify({
            title: '成功',
            message: '更新数据成功!',
            type: 'success',
            duration: 2000
          })
        })
      }

    },
    handleCreate() {
      this.switchStatus = true
      this.tempData = {
        'pid': 0
      }

      this.dialogStatus = 'create'
      this.dialogFormVisible = true
    },
    handleDownFormVisible() {
      this.tempData = Object.assign({}, deleteMenus)
      this.dialogFormVisible = false
    },
    // 删除
    handleDelete(scope) {
      this.$confirm('此操作将永久删除该数据, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deleteMenus(scope.row.id).then(() => {
          this.queryDatalist = []
          this.GetList()
          this.$message({
            type: 'success',
            message: '删除成功!'
          })
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

<style scoped>

</style>
