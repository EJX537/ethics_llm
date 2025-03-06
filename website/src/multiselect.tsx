import { createSignal, createEffect, For, Show, onMount } from "solid-js";

export interface Option {
    value: string;
    label: string;
}

interface MultiSelectProps {
    options?: Option[];
    placeholder?: string;
    onChange?: (selected: Option[]) => void;
    initialSelected?: Option[];
    maxSelections?: number;
}

const MultiSelect = (props: MultiSelectProps) => {
    const {
        options = [],
        placeholder = "Select options...",
        onChange = () => { },
        initialSelected = [],
        maxSelections = Infinity,
    } = props;

    const [selectedOptions, setSelectedOptions] = createSignal(initialSelected);
    const [isOpen, setIsOpen] = createSignal(false);
    const [searchText, setSearchText] = createSignal("");
    const [filteredOptions, setFilteredOptions] = createSignal(options);
    let containerRef: HTMLDivElement | undefined;
    let selectorRef: HTMLInputElement | undefined;


    // Update filtered options when search text or options change
    createEffect(() => {
        if (searchText() === "") {
            setFilteredOptions(options);
        } else {
            setFilteredOptions(
                options.filter((option) =>
                    option.label.toLowerCase().includes(searchText().toLowerCase())
                )
            );
        }
    });

    // Notify parent component when selection changes
    createEffect(() => {
        onChange(selectedOptions());
    });

    // Handle clicks outside the component to close dropdown
    onMount(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (containerRef && !containerRef.contains(event.target as Node) && isOpen()) {
                setIsOpen(false);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);

        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    });

    // Update the toggleOption function
    const toggleOption = (option: Option) => {
        const currentSelected = selectedOptions();
        const isSelected = currentSelected.some((item) => item.value === option.value);

        if (isSelected) {
            setSelectedOptions(
                currentSelected.filter((item) => item.value !== option.value)
            );
        } else {
            // Only add if we haven't reached the limit
            if (currentSelected.length < maxSelections) {
                const newSelected = [...currentSelected, option];
                setSelectedOptions(newSelected);

                // Close dropdown if max selections reached
                if (newSelected.length >= maxSelections) {
                    setIsOpen(false);
                    setSearchText(""); // Clear search text too
                }
            }
        }
    };

    const removeOption = (option: Option, e: Event) => {
        e.stopPropagation();
        setSelectedOptions(
            selectedOptions().filter((item) => item.value !== option.value)
        );
    };

    const handleKeyDown = (e: KeyboardEvent) => {
        if (e.key === "Escape") {
            setIsOpen(false);
        }
    };
    return (
        <div class="relative w-full" ref={containerRef}>
            <div
                class="flex flex-wrap items-center min-h-10 p-2 border border-gray-300 rounded bg-white cursor-text"
                onClick={() => {
                    setIsOpen(true);
                    selectorRef?.focus();
                }}
            >
                <For each={selectedOptions()}>
                    {(option) => (
                        <div class="flex items-center bg-blue-100 text-blue-800 text-sm font-medium mr-2 mb-1 px-2 py-1 rounded">
                            {option.label}
                            <button
                                type="button"
                                class="ml-1 text-blue-600 hover:text-blue-800 focus:outline-none"
                                onClick={(e) => removeOption(option, e)}
                            >
                                &times;
                            </button>
                        </div>
                    )}
                </For>

                <input
                    ref={selectorRef}
                    type="text"
                    class="flex-grow outline-none text-sm min-w-20"
                    placeholder={
                        selectedOptions().length === 0
                            ? placeholder
                            : selectedOptions().length >= maxSelections
                                ? `Maximum ${maxSelections} items selected`
                                : ""
                    }
                    value={searchText()}
                    onInput={(e) => setSearchText(e.currentTarget.value)}
                    onKeyDown={handleKeyDown}
                    onFocus={() => setIsOpen(true)}
                    disabled={selectedOptions().length >= maxSelections}
                />
            </div>

            <Show when={isOpen()}>
                <div class="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded shadow-lg max-h-60 overflow-y-auto">
                    <Show when={selectedOptions().length >= maxSelections}>
                        <div class="px-4 py-2 text-amber-600 font-medium">
                            Maximum {maxSelections} items can be selected
                        </div>
                    </Show>

                    <Show when={filteredOptions().length === 0}>
                        <div class="px-4 py-2 text-gray-500">No options found</div>
                    </Show>

                    <For each={filteredOptions()}>
                        {(option) => {
                            const isSelected = () =>
                                selectedOptions().some((item) => item.value === option.value);

                            const isDisabled = () =>
                                selectedOptions().length >= maxSelections && !isSelected();

                            return (
                                <div
                                    class={`px-4 py-2 cursor-pointer hover:bg-gray-100 
                                    ${isSelected() ? "bg-blue-50" : ""}
                                    ${isDisabled() ? "opacity-50 cursor-not-allowed" : ""}`}
                                    onClick={() => !isDisabled() && toggleOption(option)}
                                >
                                    <div class="flex items-center">
                                        <input
                                            type="checkbox"
                                            class="mr-2"
                                            checked={isSelected()}
                                            disabled={isDisabled()}
                                            onChange={() => { }}
                                        />
                                        {option.label}
                                    </div>
                                </div>
                            );
                        }}
                    </For>
                </div>
            </Show>
        </div>
    );
};

export default MultiSelect;