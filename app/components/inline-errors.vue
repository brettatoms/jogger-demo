<template>
    <div>
        <p
            v-for="msg in errors"
            class="alert help-text"
        >{{ msg }}</p>
    </div>
</template>
<script>
 export default {
     props: ['errors']
 }
</script>
<style lang="scss" scoped>
 p {
     color: red;
 }
</style>
