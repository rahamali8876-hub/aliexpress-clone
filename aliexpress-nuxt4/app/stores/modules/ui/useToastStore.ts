import { defineStore } from "pinia"

export type ToastType = "success" | "error" | "info"

export const useToastStore = defineStore("toast", () => {
    const message = ref("")
    const type = ref<ToastType>("success")
    const visible = ref(false)
    let timeout: ReturnType<typeof setTimeout> | null = null

    function show(msg: string, toastType: ToastType = "success", duration = 3000) {
        message.value = msg
        type.value = toastType
        visible.value = true

        if (timeout) clearTimeout(timeout)

        timeout = setTimeout(() => {
            visible.value = false
        }, duration)
    }

    function hide() {
        visible.value = false
        if (timeout) clearTimeout(timeout)
    }

    return {
        message,
        type,
        visible,
        show,
        hide
    }
})
