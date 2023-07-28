#[macro_export]
macro_rules! cfg_initiator{
    ( $($item: item)* ) => {
        $(
            #[cfg(feature="initiator")]
            $item
        )*
    }
}

#[macro_export]
macro_rules! cfg_repeater {
    ( $($item: item)* ) => {
        $(
            #[cfg(feature="repeater")]
            $item
        )*
    };
}

#[macro_export]
macro_rules! cfg_responder {
    ( $($item: item)* ) => {
        $(
            #[cfg(feature="responder")]
            $item
        )*
    };
}
