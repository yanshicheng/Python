<template>
  <el-row>
    <el-col :span="8" style="margin-top: 20px;  margin-right: 20px; margin-left: 20px;">
      <el-card shadow="hover" class="box-card">
        <div class="clearfix" slot="header" >
          <span>信息展示</span>
        </div>
        <span data-v-38faac93="" class="el-avatar el-avatar--circle" style="height: 100px; width: 100px; line-height: 100px;"><img src="https://i.gtimg.cn/club/item/face/img/3/15643_100.gif" style="object-fit: cover;"></span>
        <div :key="o" class="text item" v-for="o in 4">
          {{ '列表内容 ' + o }}
        </div>
      </el-card>
    </el-col>


     <el-col :span="15" style="margin-top: 20px; ">
        <el-card shadow="hover" class="box-card">
         <el-tabs tab-position="left" >
    <el-tab-pane label="用户管理" >
         <el-form
           label-position="right"
           label-width="80px"
            class="infinite-list"
           :model="QueryUserInfo"
           style="line-height: 32px;"
         >
            <el-form-item label="名称">
              <el-input v-model="QueryUserInfo.name"></el-input>
            </el-form-item>
            <el-form-item label="邮箱">
              <el-input v-model="QueryUserInfo.email"></el-input>
            </el-form-item>
            <el-form-item label="手机号">
              <el-input v-model="QueryUserInfo.phone"></el-input>
            </el-form-item>
           <el-form-item label="角色">
             <el-select
                  v-model="value"
                  multiple
                  filterable
                  allow-create
                  default-first-option
                  placeholder="请选择文章标签">
                  <el-option
                    v-for="item in options"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value">
            </el-option>
            </el-select>
            </el-form-item>
                <el-form-item label="部门">
               <el-select v-model="value" placeholder="请选择">
                <el-option
                  v-for="item in options"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value">
                </el-option>
              </el-select>
            </el-form-item>
           <el-form-item label="备注" >
              <el-input type="textarea" v-model="QueryUserInfo.remarks"></el-input>
            </el-form-item>

      </el-form>
      <el-button type="primary" style="margin-top: 10px; float: right">提交</el-button>
    </el-tab-pane>

    <el-tab-pane label="重置密码">配置管理</el-tab-pane>
    <el-tab-pane label="待定">待定</el-tab-pane>
    <el-tab-pane label="待定">待定</el-tab-pane>
  </el-tabs>
            </el-card>
     </el-col>

  </el-row>
</template>

<script>
import {
  getInfo,
  putUserInfo,
} from "@/api/user";

export default {
  name: 'PersonalCentre',
  data() {
    return {
      QueryUserInfo: { },
      options: [{
        value: '选项1',
        label: '黄金糕'
      }]
    };
  },
  created() {
    getInfo().then(response => {
      this.QueryUserInfo = response.data
    })
  },
  methods: {
    handleClick() {
      this.$router.push({ name: 'Dashboard' })
    }
  }

}
</script>

<style scoped>

</style>
