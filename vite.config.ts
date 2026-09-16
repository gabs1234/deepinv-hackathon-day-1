export default {
  server: {
    watch: {
      // Figures are copied into public/; the linked Python project need not be watched.
      ignored: ['**/multi-distance-phase-retrieval/**'],
    },
  },
}
