import { storeToRefs } from "pinia"
import { useAddressStore } from "~/stores/modules/address/addressStore"

export function useAddress() {
    const store = useAddressStore()
    const { addresses, selectedAddress, loading, error } = storeToRefs(store)

    return {
        addresses,
        selectedAddress,
        loading,
        error,
        loadAddresses: store.loadAddresses,
        addAddress: store.addAddress
    }
}
