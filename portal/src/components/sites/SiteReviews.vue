<template>
  <div class="bg-white rounded-2xl shadow-md p-6">
    <h2 class="text-2xl font-semibold text-gray-800 mb-4 flex items-center gap-2">
      <svg class="w-6 h-6 text-yellow-500" fill="currentColor" viewBox="0 0 20 20">
        <path
          d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.175 3.63a1 1 0 00.95.69h3.812c.969 0 1.371 1.24.588 1.81l-3.084 2.24a1 1 0 00-.364 1.118l1.175 3.63c.3.921-.755 1.688-1.54 1.118l-3.084-2.24a1 1 0 00-1.176 0l-3.084 2.24c-.784.57-1.838-.197-1.539-1.118l1.175-3.63a1 1 0 00-.364-1.118L2.324 9.057c-.783-.57-.38-1.81.588-1.81h3.812a1 1 0 00.95-.69l1.175-3.63z"
        />
      </svg>
      Reseñas
    </h2>

    <template v-if="!system.reviewsEnabled">
      <div class="p-3 bg-yellow-100 text-yellow-800 rounded-lg text-sm">
        Las reseñas están temporalmente deshabilitadas.
      </div>
    </template>

    <template v-else>
      <button
        @click="handleWriteReview"
        :class="[
          'px-4 py-2 bg-yellow-500 text-white font-medium rounded-lg shadow transition hover:bg-yellow-600 cursor-pointer'
        ]"
      >
        {{ showForm ? 'Cancelar' : 'Escribir reseña' }}
      </button>

      <!-- Mostrar formulario solo si reviews están habilitadas -->
      <ReviewForm
        v-if="showForm"
        :site-id="siteId"
        @review-submitted="handleReviewSubmitted"
        class="mb-6"
      />

      <!-- Lista de reseñas -->
      <div v-if="loading" class="text-gray-500">Cargando reseñas...</div>
      <div v-else-if="error" class="text-red-500">{{ error }}</div>
      <div v-else-if="!reviews.length" class="text-gray-500">No hay reseñas todavía.</div>

      <ul v-else class="space-y-4">
        <li
          v-for="r in reviews"
          :key="r.id"
          class="border border-gray-100 rounded-xl p-4 bg-gray-50 hover:bg-gray-100 transition"
        >
          <div class="flex justify-between items-center mb-2">
            <span class="font-semibold text-gray-800">{{ getReviewerName(r) }}</span>
            <div class="flex items-center gap-2">
              <span class="text-sm text-gray-400">{{ formatDate(r.created_at) }}</span>
              <button
                v-if="isOwnReview(r)"
                @click="confirmDelete(r)"
                class="text-red-500 hover:text-red-700 text-sm font-medium transition-colors"
              >
                Eliminar
              </button>
            </div>
          </div>

          <div class="flex items-center mb-1">
            <span v-for="n in 5" :key="n" class="text-yellow-400">
              <svg
                v-if="n <= r.calificacion"
                class="w-4 h-4 inline"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.175 3.63a1 1 0 00.95.69h3.812c.969 0 1.371 1.24.588 1.81l-3.084 2.24a1 1 0 00-.364 1.118l1.175 3.63c.3.921-.755 1.688-1.54 1.118l-3.084-2.24a1 1 0 00-1.176 0l-3.084 2.24c-.784.57-1.838-.197-1.539-1.118l1.175-3.63a1 1 0 00-.364-1.118L2.324 9.057c-.783-.57-.38-1.81.588-1.81h3.812a1 1 0 00.95-.69l1.175-3.63z"
                />
              </svg>
            </span>
          </div>

          <p class="text-gray-700">{{ r.contenido }}</p>
        </li>
      </ul>

      <div
        v-if="!loading && totalPages > 1"
        class="flex justify-center items-center gap-2 mt-6"
      >
        <button
          @click="prevPage"
          :disabled="currentPage === 1"
          class="px-3 py-1 bg-gray-200 rounded-lg disabled:opacity-50 hover:bg-gray-300"
        >
          ← Anterior
        </button>

        <button
          v-for="p in totalPages"
          :key="p"
          @click="goToPage(p)"
          :class="[
            'px-3 py-1 rounded-lg',
            p === currentPage
              ? 'bg-yellow-500 text-white'
              : 'bg-gray-200 hover:bg-gray-300'
          ]"
        >
          {{ p }}
        </button>

        <button
          @click="nextPage"
          :disabled="currentPage === totalPages"
          class="px-3 py-1 bg-gray-200 rounded-lg disabled:opacity-50 hover:bg-gray-300"
        >
          Siguiente →
        </button>
      </div>

      <ConfirmModal
        :show="showDeleteModal"
        title="¿Eliminar reseña?"
        message="Esta acción no se puede deshacer. Tu reseña será eliminada permanentemente."
        @confirm="handleDelete"
        @cancel="showDeleteModal = false"
      />
    </template>
  </div>
  <LoginPopup
    v-model="showLoginPopup"
    @login="onLoginSuccess"
  />
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { toast } from 'vue-sonner'
import api from '@/api/axios'
import { useAuth } from '@/composables/useAuth'
import { useReviews } from '@/composables/useReviews'
import { useSystemStore } from '@/stores/system'
import ReviewForm from './ReviewForm.vue'
import ConfirmModal from '@/components/common/ConfirmModal.vue'
import LoginPopup from '@/components/login_google/loginPopUp.vue'
const showLoginPopup = ref(false)

const onLoginSuccess = (user) => {
  console.log("Usuario logueado:", user)
  showLoginPopup.value = false
  showForm.value = true // abre automáticamente el formulario
}
const system = useSystemStore()
const props = defineProps({
  siteId: { type: Number, required: true },
})
const { currentUser } = useAuth()
const { deleteReview } = useReviews()

const reviews = ref([])
const loading = ref(true)

const error = ref(null)
const showForm = ref(false)
const showDeleteModal = ref(false)
const reviewToDelete = ref(null)
const currentPage = ref(1)
const meta = ref({
  page: 1,
  per_page: 25,
  total: 0
})



const loadReviews = async (page = 1) => {
  loading.value = true;
  error.value = null;

  try {
    const { data } = await api.get(`/sites/${props.siteId}/reviews`, {
      params: { page, per_page: meta.value.per_page }
    })

    reviews.value = data.data
    meta.value = data.meta
    currentPage.value = page
  } catch (err) {
    console.error(err)
    error.value = 'No se pudieron cargar las reseñas.'
    toast.error('Error al cargar reseñas')
  } finally {
    loading.value = false
  }
}
const goToPage = (page) => {
  if (page < 1 || page > totalPages.value) return
  loadReviews(page)
}

const nextPage = () => goToPage(currentPage.value + 1)
const prevPage = () => goToPage(currentPage.value - 1)


const totalPages = computed(() => {
  return Math.ceil(meta.value.total / meta.value.per_page)
})

const handleWriteReview = () => {
  if (!currentUser.value) {
    showLoginPopup.value = true
    return
  }
  showForm.value = !showForm.value
}



const isOwnReview = (review) => {
  return currentUser.value && review.user_id === currentUser.value.id
}

const confirmDelete = (review) => {
  reviewToDelete.value = review
  showDeleteModal.value = true
}

const handleDelete = async () => {
  if (!reviewToDelete.value) return

  try {
    await deleteReview(props.siteId, reviewToDelete.value.id)
    showDeleteModal.value = false
    reviewToDelete.value = null
    await loadReviews(1)
  } catch (err) {
    console.error(err)
  }
}

const handleReviewSubmitted = () => {
  showForm.value = false
  loadReviews(1)
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString()
}

const getReviewerName = (review) => {
  
  return (
    review?.usuario?.nombre ||
    review?.user?.nombre ||
    review?.user?.name ||
    review?.nombre ||
    review?.author_name ||
    review?.author?.name ||
    review?.usuario_nombre ||
    'Usuario'
  )
}

onMounted(loadReviews)
</script>
