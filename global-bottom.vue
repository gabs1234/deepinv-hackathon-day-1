<template>
  <footer
    v-if="$nav.currentLayout !== 'cover'"
    class="absolute bottom-3 right-4 z-10 text-xs text-gray-400 select-none"
  >
    {{ $nav.currentPage }} / {{ $nav.total }}
  </footer>
</template>
