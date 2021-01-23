<template>
  <div>
    <el-card class="box-card" shadow="hover" style="margin: 20px">
      <div class="clearfix" slot="header">
        <span>用户管理</span>
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
            label="姓名"
            prop="name"
          >
          </el-table-column>

          <el-table-column
            align="center"
            label="邮箱"
            prop="email"
          >
          </el-table-column>
          <el-table-column align="center" label="角色">
            <template slot-scope="{row,$index}">
             <span :key="index" v-for="(item, index) in row.roles_info ">
                 <el-tag v-if="item === 'admin'">{{ item }}</el-tag>
                 <el-tag type="warning" v-else>{{ item }}</el-tag>
             </span>

            </template>
          </el-table-column>
          <el-table-column
            align="center"
            label="部门"
            prop="department_info"
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
        <el-pagination
          :current-page=pageQuerylist.page
          :page-size=pageQuerylist.limit
          :page-sizes=pageQuerylist.sizes
          :total=pageQuerylist.total
          @current-change="handleCurrentChange"
          @size-change="handleSizeChange"
          background
          layout="total, sizes, prev, pager, next, jumper"
          v-show="pageQuerylist.total>0"
        >
        </el-pagination>
      </div>
    </el-card>
    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-form :model="tempData" :rules="rules" class="el-form">
        <el-form-item label="姓名" label-width="80px" prop="name">
          <el-input v-model="tempData.name"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" label-width="80px" prop="email">
          <el-input v-model="tempData.email"></el-input>
        </el-form-item>
        <el-form-item label="密码" label-width="80px" prop="password" v-if="dialogStatus==='create'">
          <el-input placeholder="请输入密码" show-password v-model="tempData.password"></el-input>
        </el-form-item>
        <el-form-item label="确认密码" label-width="80px" prop="re_password" v-if="dialogStatus==='create'">
          <el-input placeholder="请再次输入密码" show-password v-model="tempData.re_password"></el-input>
        </el-form-item>
        <el-form-item label="手机号" label-width="80px">
          <el-input v-model="tempData.phone"></el-input>
        </el-form-item>
        <el-form-item label="状态" label-width="80px">
          <el-switch v-model="tempData.is_active"></el-switch>
        </el-form-item>
        <el-form-item label="角色" label-width="80px">
          <el-input v-model="tempData.roles_info"></el-input>
        </el-form-item>
        <el-form-item label="部门" label-width="80px">
          <el-select placeholder="选择部门" v-model="tempData.department_info">
            <el-option :key="item.id" :label="item.title" :value="item.id" v-for="item in departments"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="备注" label-width="80px">
          <el-input type="textarea" v-model="tempData.remarks"></el-input>
        </el-form-item>
      </el-form>
      <div class="dialog-footer" slot="footer">
        <el-button @click="handleDownFormVisible()">取 消</el-button>
        <el-button @click="dialogStatus==='create'?createData():updateData()" type="primary">确 定</el-button>

      </div>
    </el-dialog>

    <el-drawer
      :before-close="cancelForm"
      :visible.sync="dialog"
      custom-class="demo-drawer"
      direction="rtl"
      title="编辑用户"
    >
      <div class="demo-drawer__content">
        <el-form :model="tempData" class="el-form">
          <el-form-item label="姓名" label-width="80px">
            <el-input style="width: 350px" v-model="tempData.name"></el-input>
          </el-form-item>
          <el-form-item label="邮箱" label-width="80px">
            <el-input style="width: 350px" v-model="tempData.email"></el-input>
          </el-form-item>
          <el-form-item label="手机号" label-width="80px">
            <el-input style="width: 350px" v-model="tempData.phone"></el-input>
          </el-form-item>
          <el-form-item label="状态" label-width="80px">
            <el-switch v-model="tempData.is_active"></el-switch>
            <!--        <el-input v-model="tempData.is_active" style="width: 350px"></el-input>-->
          </el-form-item>
          <el-form-item label="角色" label-width="80px">
            <el-input style="width: 350px" v-model="tempData.roles_info"></el-input>
          </el-form-item>
          <el-form-item label="部门" label-width="80px">
            <!--        <el-input v-model="tempData.department_info" style="width: 350px"></el-input> tempData.department_info-->
            <el-select placeholder="选择部门" v-model="tempData.department_info">
              <el-option :key="item.id" :label="item.title" :value="item.id" v-for="item in departments"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="备注" label-width="80px">
            <el-input style="width: 350px" type="textarea" v-model="tempData.remarks"></el-input>
          </el-form-item>
        </el-form>
        <div class="demo-drawer__footer">
          <el-button @click="cancelForm" style="margin-left: 20px; ">取 消</el-button>
          <el-button @click="updateData" class="el-button el-button--primary" type="primary">确 定</el-button>
        </div>
      </div>

    </el-drawer>

  </div>


</template>

<script>
import {
  getDepartment
} from "@/api/user";
import {
  getUserManagement,
  postUserManagement,
  putUserManagement,
  deleteUserManagement,
  detailsUserManagement
} from "@/api/user";

export default {
  name: 'PersonalCentre',
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
    const validateisEmail = (rule, value, callback) => {
      const reg = '^([a-zA-Z0-9]+[-_\.]?)+@[a-zA-Z0-9]+\.[a-z]+$';
      if (value === '' || value === undefined || value === null) {
        callback();
      } else {
        if (!reg.test(value)) {
          callback(new Error('请输入正确的邮箱地址'));
        } else {
          callback();
        }
      }
    }
    const validateisPhone = (rule, value, callback) => {
      const reg = '^[1][3,4,5,7,8][0-9]{9}$';
      if (value === '' || value === undefined || value === null) {
        callback()
      } else {
        if ((!reg.test(value)) && value !== '') {
          callback(new Error('请输入正确的电话号码'))
        } else {
          callback()
        }
      }
    }
    return {
      rules: {
        name: [{required: true, message: '用户名必填', trigger: 'blur'}],
        email: [{required: true, message: '邮箱必填', validator: validateisEmail}],
        phone: [{required: true, message: '邮箱必填', validator: validateisPhone}],
        password: [{required: true, trigger: 'blur', validator: validatePassword}],
        re_password: [{required: true, trigger: 'blur', validator: validateRePassword}]
      },
      pageQuerylist: {
        page: 1,
        size: 10,
        total: 0,
        sizes: [10, 20, 30, 40, 50],
        search_content: ''
      },
      queryDatalist: {},
      dialogFormVisible: false,
      textMap: {
        update: '更新信息',
        create: '创建部门'
      },
      dialog: false,
      tempData: {},
      departments: {}
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
    getDepartments() {
      getDepartment().then((request) => {
        this.departments = request.data
      })
    },
    GetList() {
      getUserManagement({
        search_content: this.pageQuerylist.search_content,
        page: this.pageQuerylist.page,
        size: this.pageQuerylist.size
      }).then(response => {
        this.queryDatalist = response.data
        this.pageQuerylist.total = response.count
      })
    },
    handlEdit(row) {
      // console.log(row)
      // this.tempData.department = row.department_info
      // this.email = row.email
      // this.id = row.id
      // this.is_active = row.is_active
      // this.name = row.name
      // this.phone = row.phone
      // this.remarks = row.remarks
      // for (var item in row.roles_info) {
      //   this.roles.push(item)
      // }
      this.tempData = JSON.parse(JSON.stringify(row))
      // this.dialogStatus = 'update'
      this.getDepartments()
      this.dialog = true
    },
    createData() {
      postUserManagement({
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
        name: this.tempData.name,
        email: this.tempData.email,
        phone: this.tempData.phone,
        is_active: this.tempData.is_active,
        roles: this.tempData.roles_info,
        department: this.tempData.department_info,
        remarks: this.tempData.remarks
      }
      putUserManagement(jsonParams, this.tempData.id).then(() => {
        this.GetList()
        this.tempData = {}
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
      this.tempData = {}
      this.getDepartments()
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
        deleteUserManagement(row.id).then(() => {
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
    handleClose(done) {
      if (this.loading) {
        return;
      }
      this.$confirm('确定要提交表单吗？')
        .then(_ => {
          this.loading = true;
          this.timer = setTimeout(() => {
            done();
            // 动画关闭需要一定的时间
            setTimeout(() => {
              this.loading = false;
            }, 400);
          }, 2000);
        })
        .catch(_ => {
        });
    },
    cancelForm() {
      this.dialog = false
    }
  },
}
</script>

<style scoped>

</style>
