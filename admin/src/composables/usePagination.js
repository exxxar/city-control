import { ref, computed } from 'vue'

export function usePagination(initialPage = 1, perPage = 20) {
    const page = ref(initialPage)
    const per_page = ref(perPage)
    const total = ref(0)
    const pages = ref(0)

    const hasNext = computed(() => page.value < pages.value)
    const hasPrev = computed(() => page.value > 1)

    function updatePagination(response) {
        if (response?.total !== undefined) {
            total.value = response.total
            pages.value = response.pages || Math.ceil(response.total / per_page.value)
            page.value = response.page || page.value
        }
    }

    function goToPage(p) {
        if (p >= 1 && p <= pages.value) {
            page.value = p
        }
    }

    function next() {
        if (hasNext.value) page.value++
    }

    function prev() {
        if (hasPrev.value) page.value--
    }

    function getParams() {
        return {
            page: page.value,
            per_page: per_page.value
        }
    }

    return {
        page,
        per_page,
        total,
        pages,
        hasNext,
        hasPrev,
        updatePagination,
        goToPage,
        next,
        prev,
        getParams
    }
}