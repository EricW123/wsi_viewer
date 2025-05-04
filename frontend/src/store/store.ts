import { legacy_createStore as createStore } from 'redux'

export interface AppState {
    sidebarShow: boolean
    theme: string
}

const initialState: AppState = {
    sidebarShow: true,
    theme: 'light',
}

interface Action {
    type: string
    [key: string]: string | boolean
}

function reducer(state: AppState = initialState, { type, ...rest }: Action): AppState {
    switch (type) {
        case 'set':
            return { ...state, ...rest }
        default:
            return state
    }
}

export const store = createStore(reducer)
