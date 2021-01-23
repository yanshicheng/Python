<template>
  <el-card class="box-card" shadow="hover" style="margin: 20px">
    <div class="clearfix" slot="header">
      <span>部门管理</span>
    </div>
    <div class="filter-container">
            <el-input
              v-model="pageQuerylist.search_content"
              clearable
              placeholder="请输入搜索内容"
              class="input-with-select"
              style="width: 500px"
              @keyup.enter.native="searchFilter"
            >
              <el-button slot="append" icon="el-icon-search" @click="searchFilter" />
            </el-input>
            <el-button
        @click="handleCreate"
        icon="el-icon-edit"
        class="el-button filter-item el-button--primary"
        style="margin-left: 10px;height: 35px"
        type="primary"
      >
        新建
      </el-button>
          </div>
    <div class="text item">
      <el-table
        :data="QueryUserInfo"
        border

        style="width: 100%">
        <el-table-column
          label="序号"
          type="index"
          width="80">
           </el-table-column>

        <el-table-column
          label="名称"
          align="center"
          prop="title"
        >
           </el-table-column>

        <el-table-column
          label="人数"
          align="center"
          prop="count"
        >
        </el-table-column>
        <el-table-column align="center" class-name="small-padding fixed-width" label="操作" width="180">
          <template slot-scope="{row,$index}">
            <el-button @click="handleFormVisible(row)" size="mini" type="primary">
              编辑
            </el-button>
            <el-button @click="handleDelete(row,$index)" size="mini" type="danger">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
          background
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          v-show="pageQuerylist.total>0"
          :total=pageQuerylist.total
          :current-page=pageQuerylist.page
          :page-sizes=pageQuerylist.sizes
          :page-size=pageQuerylist.limit
          layout="total, sizes, prev, pager, next, jumper"
        >
        </el-pagination>
    </div>
    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible" >
<el-form ref="form" :model="tempData" label-width="80px">
  <el-form-item label="名称">
    <el-input v-model="tempData.title"></el-input>
  </el-form-item>
    <el-form-item label="人数">
    <el-input v-model="tempData.count"></el-input>
  </el-form-item>
</el-form>
      <div class="dialog-footer" slot="footer">
        <el-button @click="handleDownFormVisible()"  >取 消</el-button>
        <el-button @click="dialogStatus==='create'?createData():updateData()" type="primary">确 定</el-button>

      </div>
    </el-dialog>
  </el-card>

</template>

<script>
import {
  getDepartment,
  putDepartment,
  deleteDepartment,
  postDepartment
} from "@/api/user";

export default {
  name: 'PersonalCentre',
  data() {
    return {
      pageQuerylist: {
        page: 1,
        size: 10,
        total: 0,
        sizes: [10, 20, 30, 40, 50],
        search_content: ''
      },
      QueryUserInfo: {
      },
      dialogFormVisible: false,
      textMap: {
        update: '更新信息',
        create: '创建部门'
      },
      tempData: {},
      dialogStatus: 'create',
    };
  },
  created() {
    this.GetList()
  },
  methods: {
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
    GetList() {
      getDepartment({
        search_content: this.pageQuerylist.search_content,
        page: this.pageQuerylist.page,
        size: this.pageQuerylist.size
      }).then(response => {
        console.log(response)
        this.QueryUserInfo = response.data
        this.pageQuerylist.total = response.count
      })
    },
    handleFormVisible(row) {
      this.tempData = JSON.parse(JSON.stringify(row))
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
    },
    createData() {
      postDepartment({
        title: this.tempData.title,
        count: this.tempData.count
      }).then((request) => {
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
      var jsonParams = {
        title: this.tempData.title,
        count: this.tempData.count
      }
      putDepartment(jsonParams, this.tempData.id).then(() => {
        this.GetList()
        this.tempData = ''
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
      // this.tempData = ''
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
    },
    handleDownFormVisible() {
      this.tempData = ''
      this.dialogFormVisible = false
    },
    // 删除
    handleDelete(row) {
      this.$confirm('此操作将永久删除该数据, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deleteDepartment(row.id).then(() => {
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
    }
  },
}
</script>

<style scoped>

</style>
