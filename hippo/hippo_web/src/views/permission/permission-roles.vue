<template>
  <div>
  <el-card class="box-card" shadow="hover" style="margin: 20px">
    <div class="clearfix" slot="header">
      <span>角色管理</span>
    </div>
    <div class="filter-container">
      <el-input
        @keyup.enter.native="searchFilter"
        class="input-with-select"
        clearable
        placeholder="请输入搜索内容"
        style="width: 500px"
        v-model="pageQuerylist.search_content"
      >
        <el-button @click="searchFilter" icon="el-icon-search" slot="append"/>
      </el-input>
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
        border
        style="width: 100%">
        <el-table-column
          label="序号"
          type="index"
          width="80">
        </el-table-column>

        <el-table-column
          align="center"
          label="名称"
          prop="title"
        >
        </el-table-column>

        <el-table-column
          align="center"
          label="标识"
          prop="slug"
        >
        </el-table-column>
        <el-table-column
          align="center"
          label="备注"
          prop="remarks"
        >
        </el-table-column>
        <el-table-column align="center" class-name="small-padding fixed-width" label="操作" width="180">
          <template slot-scope="{row,$index}">
            <el-button @click="handlEdit(row)" size="mini" type="primary">
              编辑
            </el-button>
            <el-button @click="handleDelete(row,$index)" size="mini" type="danger">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
<!--      <el-pagination-->
<!--        :current-page=pageQuerylist.page-->
<!--        :page-size=pageQuerylist.limit-->
<!--        :page-sizes=pageQuerylist.sizes-->
<!--        :total=pageQuerylist.total-->
<!--        @current-change="handleCurrentChange"-->
<!--        @size-change="handleSizeChange"-->
<!--        background-->
<!--        layout="total, sizes, prev, pager, next, jumper"-->
<!--        v-show="pageQuerylist.total>0"-->
<!--      >-->
<!--      </el-pagination>-->
    </div>
  </el-card>

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
    <el-form class="el-form" :model="tempData" >
      <el-form-item label="名称" label-width="80px" >
        <el-input v-model="tempData.title"  ></el-input>
      </el-form-item>
      <el-form-item label="标识" label-width="80px" >
        <el-input v-model="tempData.slug" ></el-input>
      </el-form-item>
      <el-form-item    label="备注" label-width="80px">
        <el-input type="textarea" v-model="tempData.remarks" ></el-input>
      </el-form-item>
      <el-form-item label="权限" label-width="80px" >
        <el-card  class="box-card">
        <el-tree
            ref="tree"
            :data="routesData"
            :props="defaultProps"
            node-key="id"
            show-checkbox
            :check-strictly="checkStrictly"
            highlight-current="true"
             @check-change="handleCheckChange"
            class="permission-tree" />
        </el-card>
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
import {
  getDepartment
} from "@/api/user";
import {getPermissionsData} from "@/api/roles";
import {
  getRoles,
  postRoles,
  putRoles,
  deleteRoles,
  detailsRoles
} from "@/api/roles";
const defaultRole = {
  title: '',
  slug: '',
  remarks: '',
  permissions: []
}
export default {

  name: 'permission-roles',
  data() {

    const validatePassword = (rule, value, callback) => {
      if (value.length < 8) {
        callback(new Error('密码输入过短请重新输入!'))
      } else {
        callback()
      }
    }
    const validateRePassword = (rule, value, callback) => {
      if (value.length < 8) {
        callback(new Error('密码输入过短请重新输入!'))
      } else if (value !== this.tempData.password) {
        callback(new Error('两次密码输入不一致请重新输入!'))
      } else {
        callback()
      }
    }
    return {
      checkStrictly: true,
      dialogStatus: 'create',
      defaultProps: {
        children: 'children',
        label: 'title'
      },
      routesData: [],
      // rules: {
      //   title: [{ required: true, message: '名称必填', trigger: 'blur' }],
      //   slug: [{ required: true, message: '标识必填', trigger: 'blur' }],
      //   permissions: [{ required: true, message: '权限必选', trigger: 'blur' }],
      // },
      pageQuerylist: {
        page: 1,
        size: 10,
        total: 0,
        sizes: [10, 20, 30, 40, 50],
        search_content: ''
      },
      queryDatalist: [],
      dialogFormVisible: false,
      textMap: {
        update: '更新信息',
        create: '创建部门'
      },
      tempData: Object.assign({}, defaultRole),
      departments: []
    };
  },
  created() {
    this.GetList()
    this.PermissionData()
  },
  methods: {
    handleCheckChange(data, checked, indeterminate) {
      const checkedKeys = this.$refs.tree.getCheckedKeys()
      this.tempData.permissions = checkedKeys
      console.log(this.tempData)
    },
    PermissionData() {
        getPermissionsData().then((request) => {
          this.routesData = request.data
        })
    },
    searchFilter() {
      this.pageQuerylist.page = 1
      this.GetList()
    },
    handleSizeChange(val) {
      this.pageQuerylist.size = val
      this.pageQuerylist.page = 1
      this.GetList()
    },
    handleCurrentChange(val) {
      this.pageQuerylist.page = val
      this.GetList()
    },
    getDepartments () {
      getDepartment().then((request) => {
        this.departments = request.data
      })
    },
    GetList() {
      getRoles({
        search_content: this.pageQuerylist.search_content,
        page: this.pageQuerylist.page,
        size: this.pageQuerylist.size
      }).then(response => {
        this.queryDatalist = response.data
        this.pageQuerylist.total = response.count
      })
    },
    handlEdit(row) {
      this.tempData = JSON.parse(JSON.stringify(row))
      console.log(row)
      this.$nextTick(() => {
        this.$refs.tree.setCheckedKeys(row.permissions);
      });
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
    },
    createData() {
      postRoles(this.tempData).then((request) => {
        this.dialogFormVisible = false
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
      putRoles(this.tempData, this.tempData.id).then(() => {
        this.GetList()
        this.tempData = []
        this.dialogFormVisible = false
        this.$notify({
          title: '成功',
          message: '更新数据成功!',
          type: 'success',
          duration: 2000
        })
      })
    },
    handleCreate() {
      this.tempData = Object.assign({}, defaultRole)
      if (this.$refs.tree) {
        this.$refs.tree.setCheckedKeys([])
      }
      console.log(111111)
      console.log(this.tempData)
      this.getDepartments()
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
    },
    handleDownFormVisible() {
      this.tempData = {}
      this.dialogFormVisible = false
    },
    // 删除
    handleDelete(row) {
      this.$confirm('此操作将永久删除该数据, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deleteRoles(row.id).then(() => {
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
  },
}
</script>

<style scoped>

</style>
