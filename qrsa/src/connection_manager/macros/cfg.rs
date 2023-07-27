#[macro_export]
macro_rules! cfg_initiator{
    ( $($item: item) * ) => {
        $(
            #[cfg(feature="initiator")]
            $item
        )*
    }
}
