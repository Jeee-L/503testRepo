<template>
    <span>flask返回的数据:</span>
    <br>
    <span>{{ this.receiveddata }}</span>
    <br>
    <span>{{ this.receiveddata['ip'] }}</span>
</template>

<script>
// references: https://blog.csdn.net/weixin_44127580/article/details/113861672
  export default {
    data () {
    	return{
        receiveddata:{},   // 获取后端发送的消息
        ip:null    
    	}
    },
    
    sockets:{    // socket.io携带，与watch/create/data等同级
      connect:function () {
          console.log('连接成功')   // 判断是否正确连接上后端
        },
        
      api:function (rdata) {    // api为对应后端发出的信息接口，可自行更换
          this.receiveddata = rdata      // 获取后端发出的信息
        }
    },
    
    mounted () {    // 在组件开始渲染时进行调用
      this.$socket.connect() // socket连接
      this.$socket.emit('testing')  // 发送消息:对应后端test测试函数
      console.log(this.$socket)
      console.log('连接中')
    },
    
    destroyed () {    // 当离开组件时，结束调用
      if (this.$socket) this.$socket.disconnect()  // 如果socket连接存在，销毁socket连接
      console.log('连接已断开')
    }
    
  }

</script>