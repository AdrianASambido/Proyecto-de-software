<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-5xl mx-auto px-4">

      <!-- 🔙 Botón Volver -->
<div class="w-40 mb-6">
        <RouterLink
          to="/"
          class="px-4 py-2 bg-white hover:bg-gray-100 text-gray-700 rounded-lg font-medium shadow-sm border flex items-center gap-2 transition"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
          Volver
        </RouterLink>
      </div>

      <h1 class="text-3xl font-bold text-gray-900 mb-6">Mis Reseñas</h1>
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p class="mt-4 text-gray-600">Cargando reseñas...</p>
      </div>

      <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
        {{ error }}
      </div>

      <div v-else-if="!reviews.length" class="bg-white rounded-lg shadow p-8 text-center">
        <p class="text-gray-600 mb-4">No has escrito ninguna reseña todavía</p>
        <router-link
          to="/sitios"
          class="inline-block px-4 py-2 bg-yellow-500 text-white rounded-lg hover:bg-yellow-600 transition-colors"
        >
          Explorar sitios
        </router-link>
      </div>

      <div v-else class="space-y-4">
        <div class="flex justify-end mb-4">
  <button
    @click="toggleSort"
    class="text-sm text-blue-600 hover:text-blue-800 font-medium transition-colors"
  >
    Ordenar: {{ sortOrderLabel }}
  </button>
</div>

        <div
          v-for="review in reviews"
          :key="review.id"
          class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
        >
          <div class="flex justify-between items-start mb-4">
            <div class="flex-1">
              <router-link
                :to="`/sitio/${review.site.id}`"
                class="text-xl font-semibold text-gray-900 hover:text-blue-600 transition-colors"
              >
                {{ review.site.nombre }}
              </router-link>
              <p class="text-sm text-gray-500 mt-1">
                {{ review.site.ciudad }}, {{ review.site.provincia }}
              </p>
            </div>

            <span
              class="px-3 py-1 rounded-full text-sm font-medium"
              :class="getEstadoBadgeClass(review.estado)"
            >
              {{ getEstadoLabel(review.estado) }}
            </span>
          </div>

          <div class="flex items-center mb-3">
            <span v-for="n in 5" :key="n" class="text-yellow-400">
              <svg
                v-if="n <= review.calificacion"
                class="w-5 h-5 inline"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.175 3.63a1 1 0 00.95.69h3.812c.969 0 1.371 1.24.588 1.81l-3.084 2.24a1 1 0 00-.364 1.118l1.175 3.63c.3.921-.755 1.688-1.54 1.118l-3.084-2.24a1 1 0 00-1.176 0l-3.084 2.24c-.784.57-1.838-.197-1.539-1.118l1.175-3.63a1 1 0 00-.364-1.118L2.324 9.057c-.783-.57-.38-1.81.588-1.81h3.812a1 1 0 00.95-.69l1.175-3.63z"
                />
              </svg>
            </span>
            <span class="ml-2 text-sm text-gray-500">
              {{ formatDate(review.created_at) }}
            </span>
          </div>

          <p class="text-gray-700 mb-4">{{ review.contenido }}</p>

          <div v-if="review.estado === 'rechazada' && review.motivo_rechazo" class="bg-red-50 border border-red-200 rounded-lg p-3 mb-4">
            <p class="text-sm font-medium text-red-800 mb-1">Motivo de rechazo:</p>
            <p class="text-sm text-red-700">{{ review.motivo_rechazo }}</p>
          </div>

          <div class="flex gap-3">
            <router-link
              :to="`/sitio/${review.site.id}`"
              class="text-blue-600 hover:text-blue-800 text-sm font-medium transition-colors"
            >
              Ver sitio
            </router-link>
            <button
              v-if="review.estado === 'pendiente'"
              @click="confirmEdit(review)"
              class="text-green-600 hover:text-green-800 text-sm font-medium transition-colors"
            >
              Editar
            </button>
            <button
              @click="confirmDelete(review)"
              class="text-red-500 hover:text-red-700 text-sm font-medium transition-colors"
            >
              Eliminar
            </button>
          </div>
        </div>

        <div v-if="meta.total > meta.per_page" class="flex justify-center items-center gap-4 mt-8">
          <button
            @click="previousPage"
            :disabled="currentPage === 1"
            class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Anterior
          </button>

          <span class="text-gray-600">
            Página {{ currentPage }} de {{ totalPages }}
          </span>

          <button
            @click="nextPage"
            :disabled="currentPage >= totalPages"
            class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Siguiente
          </button>
        </div>
      </div>

      <ConfirmModal
        :show="showDeleteModal"
        title="¿Eliminar reseña?"
        message="Esta acción no se puede deshacer. Tu reseña será eliminada permanentemente."
        @confirm="handleDelete"
        @cancel="showDeleteModal = false"
      />

      <EditReviewModal
        :show="showEditModal"
        :review="reviewToEdit"
        :loading="editLoading"
        @confirm="handleEdit"
        @cancel="showEditModal = false"
      />

      <div class="mt-8 text-center">
        <router-link
          to="/"
          class="inline-block px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
        >
          Volver a la página principal
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { toast } from 'vue-sonner'
import api from '@/api/axios'
import { useReviews } from '@/composables/useReviews'
import ConfirmModal from '@/components/common/ConfirmModal.vue'
import EditReviewModal from '@/components/common/EditReviewModal.vue'

const { deleteReview, updateReview } = useReviews()
const sortOrder = ref('desc') // desc = más recientes
const sortOrderLabel = computed(() =>
  sortOrder.value === 'desc' ? 'Más recientes' : 'Más antiguas'
)
const toggleSort = () => {
  sortOrder.value = sortOrder.value === 'desc' ? 'asc' : 'desc'
  sortReviews()
}
const sortReviews = () => {
  reviews.value.sort((a, b) => {
    const dateA = new Date(a.created_at)
    const dateB = new Date(b.created_at)
    return sortOrder.value === 'asc'
      ? dateA - dateB
      : dateB - dateA
  })
}

const reviews = ref([])
const loading = ref(true)
const error = ref(null)
const showDeleteModal = ref(false)
const reviewToDelete = ref(null)
const showEditModal = ref(false)
const reviewToEdit = ref(null)
const editLoading = ref(false)
const currentPage = ref(1)
const meta = ref({
  page: 1,
  per_page: 25,
  total: 0
})

const totalPages = computed(() => Math.ceil(meta.value.total / meta.value.per_page))

const loadMyReviews = async (page = 1) => {
  loading.value = true
  error.value = null
  try {
    const { data } = await api.get('/me/reviews', {
      params: { page, per_page: 25 }
    })
    
    reviews.value = data.data
    meta.value = data.meta
    currentPage.value = page
    sortReviews()

  } catch (err) {
    console.error(err)
    error.value = 'No se pudieron cargar tus reseñas.'
    toast.error('Error al cargar las reseñas')
  } finally {
    loading.value = false
  }
}

const previousPage = () => {
  if (currentPage.value > 1) {
    loadMyReviews(currentPage.value - 1)
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    loadMyReviews(currentPage.value + 1)
  }
}

const getEstadoLabel = (estado) => {
  const labels = {
    'pendiente': 'Pendiente',
    'aprobada': 'Aprobada',
    'rechazada': 'Rechazada'
  }
  return labels[estado] || estado
}

const getEstadoBadgeClass = (estado) => {
  const classes = {
    'pendiente': 'bg-yellow-100 text-yellow-800',
    'aprobada': 'bg-green-100 text-green-800',
    'rechazada': 'bg-red-100 text-red-800'
  }
  return classes[estado] || 'bg-gray-100 text-gray-800'
}

const confirmDelete = (review) => {
  reviewToDelete.value = review
  showDeleteModal.value = true
}

const handleDelete = async () => {
  if (!reviewToDelete.value) return

  try {
    await deleteReview(reviewToDelete.value.site_id, reviewToDelete.value.id)
    showDeleteModal.value = false
    reviewToDelete.value = null
    await loadMyReviews(currentPage.value)
  } catch (err) {
    console.error(err)
  }
}

const confirmEdit = (review) => {
  reviewToEdit.value = review
  showEditModal.value = true
}

const handleEdit = async (data) => {
  if (!reviewToEdit.value) return

  editLoading.value = true
  try {
    await updateReview(reviewToEdit.value.site_id, reviewToEdit.value.id, data)
    showEditModal.value = false
    reviewToEdit.value = null
    await loadMyReviews(currentPage.value)
  } catch (err) {
    console.error(err)
  } finally {
    editLoading.value = false
  }
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('es-AR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

onMounted(loadMyReviews)
</script>
